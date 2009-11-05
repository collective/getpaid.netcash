#!/usr/bin/make
#
# Makefile for getpaid.ogone
#
# $Id: Makefile 6656 2007-02-12 18:27:14Z jfroche $
PYTHON=/opt/python2.4.3/bin/python2.4
ZOPE_HOME="/usr/lib/zope2.9.6"
SOFTWARE_HOME="/usr/lib/zope2.9.6/lib/python"
PYTHONPATH:=$(PYTHONPATH):$(SOFTWARE_HOME)

translations: extract-translations update-translations

.PHONY: extract-translations
extract-translations:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) i18nextract -d getpaid.vcs -o i18n -p ../

.PHONY: update-translations
update-translations:
	msgmerge -U getpaid.netcash-fr.po getpaid.netcash.pot
