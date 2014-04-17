##############################################################################
#
# Copyright (C) Zenoss, Inc. 2014, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################
"""
Custom ZenPack initialization code. All code defined in this module will be
executed at startup time in all Zope clients.
"""
import Globals
import os.path
import simplejson
from Products.ZenModel.ZenossSecurity import ZEN_COMMON
from Products.ZenUtils.Utils import zenPath


#skinsDir= os.path.join( os.path.dirname(__file__), 'skins' )
#from Products.CMFCore.DirectoryView import registerDirectory
#if os.path.isdir(skinsDir):
#    registerDirectory("skins", globals())

def getJSONReportList(self, path='/Device Reports'):
            """
            Given a report class path, returns a list of links to child
            reports in a format suitable for a TableDatasource.
            """

            # This function will be monkey-patched onto zport, so
            # references to self should be taken as referring to zport

            # Add the base path to the path given
            path = '/zport/dmd/Reports/' + path.strip('/')

            # Create the empty structure of the response object
            response = { 'columns': ['Report'], 'data': [] }

            # Retrieve the ReportClass object for the path given. If
            # nothing can be found, return an empty response
            try:
                reportClass = self.dmd.unrestrictedTraverse(path)
            except KeyError:
                return simplejson.dumps(response)

            # Get the list of reports under the class as (url, title) pairs
            reports = reportClass.reports()
            reportpairs = [(r.absolute_url_path(), r.id) for r in reports]

            # Iterate over the reports, create links, and append them to
            # the response object
            for url, title in reportpairs:
                link = "<a href='%s'>%s</a>" % (url, title)
                row = { 'Report': link }
                response['data'].append(row)

            # Serialize the response and return it
            return simplejson.dumps(response)

        # Monkey-patch onto zport
        from Products.ZenModel.ZentinelPortal import ZentinelPortal
        ZentinelPortal.getJSONReportList = getJSONReportList

from Products.ZenModel.ZenPack import ZenPackBase

class ZenPack(ZenPackBase):
    """
    Portlet ZenPack class
    """
    def _registerReportListPortlet(self, app):
        zpm = app.zport.ZenPortletManager
        portletsrc = zenPath('Products', 'ReportListPortletPack',
                           'ReportListPortlet.js')
        zpm.register_portlet(
            sourcepath=portletsrc,
            id='ReportListPortlet',
            title='Report List',
            permission=ZEN_COMMON)

    def install(self, app):
    	ZenPackBase.install(self, app)
    	self._registerReportListPortlet(app)

    def upgrade(self, app):
    	ZenPackBase.upgrade(self, app)
    	self._registerReportListPortlet(app)

    def remove(self, app):
    	ZenPackBase.remove(self, app) zpm =
    	app.zport.ZenPortletManager
    	zpm.unregister_portlet('ReportListPortlet')
