# -*- coding: utf-8 -*-

import tempfile
import pathlib
import time
import shutil
import platform
import os
import subprocess
import io
import sys
import warnings
from typing import Optional, List

from jinja2 import Environment, FileSystemLoader

class Ebook:

    def __init__(self, path: str, title: str, author = 'ruhuayan.github.io'):
        self.output_path = path # pathlib.Path(tempfile.gettempdir()) / str(time.time())
        self.title = title
        self.author = author
        self._templates_env = Environment(loader=FileSystemLoader(
            str(pathlib.Path(__file__).parent / 'templates/')))
        
        self.chapters = list()
        self.chapter_order = 0
        self._headings = None

    def _render_file(self, template_name: str, context: dict, filename: str):
        template = self._templates_env.get_template(template_name)
        with open(os.path.join(self.output_path, filename), mode="w", encoding='utf-8') as f:
            f.write(template.render(**context))

    def setTitle(self, title: str):
        self.title = title

    def setAuthor(self, author: str):
        self.author = author

    def save_cover(self) -> None:
        if self.cover_path:
            cover_path = self.cover_path
            shutil.copy(cover_path, str(self.output_path))
        else:
            cover = pathlib.Path(__file__).parent / 'templates/cover.jpg'
            shutil.copy(str(cover), str(self.output_path))

    def create_chapter(self, chapter_title: str, filepath: str):
        self.chapter_order = self.chapter_order + 1
        chapter = dict(title = chapter_title, path = filepath, play_order = self.chapter_order)
        self.chapters.append(chapter)

    def _render_toc_ncx(self):
        ncx = 'toc.ncx'
        self._render_file(
            'toc.xml',
            {
                'chapters': self.chapters,
                'title': self.title,
                'author': self.author
            },
            ncx
        )
        return ncx

    def _render_toc_html(self):
        toc = 'toc.html'
        self._render_file(toc, {'chapters': self.chapters}, toc)
        return toc

    def _render_opf(self) -> str:
        opf_file = '{}.opf'.format(self.title)
        self._render_file(
            'opf.xml',
            {
                'chapters': self.chapters,
                'title': self.title,
                'author': self.author
            },
            opf_file
        )
        return opf_file

    def save(self) -> None:
        self._render_toc_ncx()
        self._render_toc_html()
        opf_file = self._render_opf()
        #self.save_cover()
        rc = subprocess.call([
            'ebook-convert', os.path.join(self.output_path, opf_file), os.path.join(self.output_path, '{}.mobi'.format(self.title)) 
        ])
        if rc != 0:
            raise Exception('ebook-convert failed')
