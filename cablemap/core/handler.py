# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2015 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# License: BSD, see LICENSE.txt for more details.
#
"""\
This module defines a event handlers to process cables.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from __future__ import absolute_import
import logging
import urllib
from .utils import cables_from_source, titlefy
from .interfaces import ICableHandler, implements


class NoopCableHandler(object):
    """\
    `ICableHandler` implementation which does nothing.
    """
    implements(ICableHandler)
    
    def __getattr__(self, name):
        def noop(*args): pass
        return noop


class DelegatingCableHandler(object):
    """\
    A `ICableHandler` which delegates all events to an underlying
    `ICableHandler` instance.
    """
    implements(ICableHandler)

    def __init__(self, handler):
        """\
        `handler`
            The ICableHandler instance which should receive the events.
        """
        self._handler = handler

    def __getattr__(self, name):
        return getattr(self._handler, name)


class LoggingCableHandler(object):
    """\
    A `ICableHandler` which logs all events and delegates the events to
    an underlying `ICableHandler` instance.
    """
    implements(ICableHandler)
    
    def __init__(self, handler, level='info'):
        """\

        `handler`
            The ICableHandler instance which should receive the events.
        `level`
            The logging level (default: 'info')
        """
        self._handler = handler
        self.level = level

    def __getattr__(self, name):
        def logme(*args):
            getattr(logging, self.level)('%s%r' % (name, args))
            getattr(self._handler, name)(*args)
        return logme


class TeeCableHandler(object):
    """\
    A `ICableHandler` which delegates the events to two underlying `ICableHandler`
    instances.
    """
    implements(ICableHandler)

    def __init__(self, first, second):
        """\

        `first`
            The ICableHandler instance which should receive the events first.
        `second`
            The ICableHandler which receives the events after the first handler.
        """
        self._first = first
        self._second = second

    def __getattr__(self, name):
        def delegate(*args):
            getattr(self._first, name)(*args)
            getattr(self._second, name)(*args)
        return delegate


class MultipleCableHandler(object):
    """\
    A `ICableHandler` which delegates the events to multiple underlying `ICableHandler`
    instances.
    """
    implements(ICableHandler)

    def __init__(self, handlers):
        """\

        `handlers`
            An iterable of ICableMapHandler instances.
        """
        self._handlers = tuple(handlers)

    def __getattr__(self, name):
        def delegate(*args):
            for handler in self._handlers:
                getattr(handler, name)(*args)
        return delegate


class CableIdFilter(DelegatingCableHandler):
    """\
    `DelegatingCableHandler` which delegates those `ICableHandler` events to the
    underlying handler where a predicate returns ``True``.

    Cables are filtered by their canonical identifier.
    """
    def __init__(self, handler, predicate):
        """\
        Creates the `CableIdFilter` handler.

        `handler`
            The `ICableHandler` which should receive the events.
        `predicate`
            A function which accepts a canonical cable identifier and
            returns either ``True`` or ``False``. If the predicate returns
            ``True``, the `handler` receives all events for the current
            cable.
        """
        super(CableIdFilter, self).__init__(handler)
        self._predicate = predicate
        self._accept = False

    def start(self):
        self._handler.start()

    def end(self):
        self._handler.end()

    def start_cable(self, reference_id, canonical_id):
        self._accept = self._predicate(canonical_id)
        if self._accept:
            self._handler.start_cable(reference_id, canonical_id)

    def __getattr__(self, name):
        def noop(*args): pass
        if self._accept:
            return super(CableIdFilter, self).__getattr__(name)
        return noop


class DefaultMetadataOnlyFilter(DelegatingCableHandler):
    """\
    ICableHandler implementation that acts as filter to omit the
    header and content of a cable. Further, it generates optionally titlefied
    subjects, and filters WikiLeaks IRIs != http://wikileaks.org/cable/<year>/<month>/<reference-id>.html
    """
    def __init__(self, handler, titlefy_subject=True):
        """\

        `handler`
            The ICableHandler which should receive the (filtered) events.
        `titlefy_subject`
            Indicates if the subjects should be titlefied (default: ``True``).
        """
        super(DefaultMetadataOnlyFilter, self).__init__(handler)
        if titlefy_subject:
            self.handle_subject = self._handle_subject_titlefy

    def handle_wikileaks_iri(self, iri):
        if iri.startswith(u'http://wikileaks.org') and iri.endswith(u'html'):
            self._handler.handle_wikileaks_iri(iri)

    def _handle_subject_titlefy(self, subject):
        self._handler.handle_subject(titlefy(subject))

    def handle_release_date(self, date):
        # This info isn't that interesting anymore since the lastest
        # release uses "2011-08-30" for all cables.
        pass

    def handle_content(self, content):
        pass

    def handle_header(self, header):
        pass


class DebitlyFilter(DelegatingCableHandler):
    """\
    `DelegatingCableHandler` implementation that expands `bit.ly <http://bit.ly>`_ media IRIs
    """
    def __init__(self, handler):
        """\

        `handler`
            The ICableHandler which should receive the (filtered) events.
        """
        super(DebitlyFilter, self).__init__(handler)
        self._bitly2url = {
            # For some reason this returns 404, acc. to <http://knowurl.com/>
            # the IRI is:
            u'http://bit.ly/mDfYBE': u'http://www.haiti-liberte.com/archives/volume4-46/Les%20c%C3%A2bles%20de%20WikiLeaks%20sur%20Ha%C3%AFti%20publi%C3%A9s%20par%20Ha%C3%AFti%20Libert%C3%A9.asp'
        }

    def handle_media_iri(self, iri):
        class HeadRequest(urllib2.Request):
            def get_method(self):
                return 'HEAD'
        if iri.startswith(u'http://bit.ly'):
            if not iri in self._bitly2url:
                request = HeadRequest(iri)
                try:
                    response = urllib2.urlopen(request)
                    self._bitly2url[iri] = response.geturl()
                except urllib2.HTTPError:
                    pass
            iri = self._bitly2url.get(iri, iri)
        self._handler.handle_media_iri(iri)


def handle_cable(cable, handler, standalone=True):
    """\
    Emits event from the provided `cable` to the handler.

    `cable`
        A cable object.
    `handler`
        A ICableHandler instance.
    `standalone`
        Indicates if a `start` and `end` event should be
        issued (default: ``True``).
        If `standalone` is set to ``False``, no ``handler.start()``
        and ``handler.end()`` event will be issued.
    """
    def datetime(dt):
        date, time = dt.split(u' ')
        if len(time) == 5:
            time += u':00'
        time += u'Z'
        return u'T'.join([date, time])
    if standalone:
        handler.start()
    handler.start_cable(cable.reference_id, cable.canonical_id)
    for iri in cable.wl_uris:
        handler.handle_wikileaks_iri(iri)
    handler.handle_creation_datetime(datetime(cable.created))
    if cable.released:
        handler.handle_release_date(cable.released[:10])
    if cable.nondisclosure_deadline:
        handler.handle_nondisclosure_deadline(cable.nondisclosure_deadline)
    if cable.transmission_id:
        handler.handle_transmission_id(cable.transmission_id)
    if cable.subject:
        handler.handle_subject(cable.subject)
    if cable.summary:
        handler.handle_summary(cable.summary)
    if cable.comment:
        handler.handle_comment(cable.comment)
    handler.handle_header(cable.header)
    handler.handle_content(cable.content)
    handler.handle_origin(cable.origin)
    handler.handle_classification(cable.classification)
    handler.handle_partial(cable.partial)
    for cat in cable.classification_categories:
        handler.handle_classification_category(cat)
    for classificationist in cable.classificationists:
        handler.handle_classificationist(classificationist)
    for signer in cable.signers:
        handler.handle_signer(signer)
    for tag in cable.tags:
        handler.handle_tag(tag)
    for iri in cable.media_uris:
        handler.handle_media_iri(iri)
    for rec in cable.recipients:
        handler.handle_recipient(rec)
    for rec in cable.info_recipients:
        handler.handle_info_recipient(rec)
    for ref in cable.references:
        handler.handle_reference(ref)
    handler.end_cable()
    if standalone:
        handler.end()

def handle_cables(cables, handler):
    """\
    Issues one ``handler.start()`` event, processes all `cables` and
    issues a ``handler.end()`` event.

    `cables`
        An iterable of Cable objects.
    `handler`
        The `ICableHandler` instance which should receive the events.
    """
    handler.start()
    for cable in cables:
        handle_cable(cable, handler, False)
    handler.end()


def handle_source(path, handler, predicate=None):
    """\
    Reads all cables from the provided source and issues events to
    the `handler`.

    `path`
        Either a directory with cable files or a CSV file.
    `handler`
        The `ICableHandler` instance which should receive the events.
    `predicate`
        A predicate that is invoked for each cable reference identifier.
        If the predicate evaluates to ``False`` the cable is ignored.
        By default, all cables are used.
        I.e. ``handle_source('cables.csv', handler, lambda r: r.startswith('09'))``
        would return cables where the reference identifier starts with ``09``.
    """
    handle_cables(cables_from_source(path, predicate), handler)
