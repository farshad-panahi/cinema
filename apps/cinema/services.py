import abc
import os
from django.template.loader import get_template
from weasyprint import HTML
from django.conf import settings
from ebooklib import epub
from django.template import Template


class RecipeFactory(abc.ABC):
    @abc.abstractmethod
    def factory_method(self):
        pass


class PdfFactory(RecipeFactory):
    def factory_method(self):
        return PdfGenerator()


class EpubFactory(RecipeFactory):
    def factory_method(self):
        return EpubGenerator()


class FileGenerator(abc.ABC):
    def __init__(self) -> None:
        self.template = get_template("cinema/ticket.html")

    @abc.abstractmethod
    def operation(self):
        pass


class PdfGenerator(FileGenerator):
    def operation(self, request, context):
        os.makedirs(os.path.dirname(settings.OUTPUT_FILE_PATH), exist_ok=True)
        HTML(string=self.template.render(context=context)).write_pdf(
            settings.OUTPUT_FILE_PATH
        )
        pdf_url = request.build_absolute_uri(settings.OUTPUT_ABS_URL)
        return pdf_url


class EpubGenerator(FileGenerator):
    def operation(self, request, context):
        os.makedirs(os.path.dirname(settings.OUTPUT_FILE_PATH), exist_ok=True)
        book = epub.EpubBook()

        book.set_title(context.get("title", "My Epub Book"))
        book.set_language("en")
        book.add_author(context.get("author", "Unknown Author"))

        for index, chapter_content in enumerate(context.get("chapters", [])):
            chapter_title = chapter_content.get("title", f"Chapter {index + 1}")
            chapter_content_html = chapter_content.get("content", "")

            chapter = epub.EpubHtml(
                title=chapter_title, file_name=f"chapter_{index + 1}.xhtml", lang="en"
            )
            chapter.set_content(Template(chapter_content_html).render(context))
            book.add_item(chapter)
            book.spine.append(chapter)

        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        epub_file_path = settings.OUTPUT_FILE_PATH.replace(".pdf", ".epub")
        epub.write_epub(epub_file_path, book)
        epub_url = request.build_absolute_uri(
            settings.OUTPUT_ABS_URL.replace(".pdf", ".epub")
        )
        return epub_url


def recipe_generator(request, context: dict):
    factories = {"pdf": PdfFactory, "epub": EpubFactory}
    file_format = context["frmt"]

    output_generator = factories[file_format]().factory_method()
    output = output_generator.operation(request, context)

    return output
