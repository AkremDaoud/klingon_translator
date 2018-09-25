# Klingon_translator

A tool allowing to translate a name written in English to Klingon and find out its species using http://stapi.co.

## Requirements

* [**stapi-python**](https://github.com/mklucz/stapi-python) A client for the Star Trek API
* [**requests**] (https://github.com/requests/requests) Requests: HTTP for Humans
* [**Git**](https://git-scm.com) Source Control

## Setup

```bash
$ git clone https://github.com/AkremDaoud/klingon_translator.git
$ cd klingon_translator.git/src
$ chmod +rwx *.py
```

## Usage

In the first parameter is the name of any Star Treck character (it can have spaces between words).
As output, his name will be translated in Klingon written using the correspondent hexadecimal numbers and his species.

```bash
$ python translate_main.py Uhura
0xF8E5 0xF8D6 0xF8E5 0xF8E1 0xF8D0
Human 
```
