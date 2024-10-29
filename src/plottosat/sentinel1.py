import ee
from datetime import datetime
from dataclasses import dataclass

class Sentinel1Config

class Sentinel1:
    
    def __init__(self, 
                 geometry, 
                 config, 
                 masks, 
                 applyAspects):
        self.startDate = datetime.strptime(config["startDate"], "%Y-%m-%d").date
        self.endDate   = datetime.strptime(config["endDate"], "%Y-%m-%d").date

        self.sentinel1 = ee.ImageCollection('COPERNICUS/S1_GRD') \
                           .filterDate(self.startDate, self.endDate) \
                           .filterBounds(geometry) \
                           .filter(ee.Filter.listContains('transmitterReceiverPolarisation','VV')) \
                           .filter(ee.Filter.listContains('transmitterReceiverPolarisation','VH')) \
                           .filter(ee.Filter.eq('instrumentMode', 'IW'))

        # apply water and land mask
        # create forest lost mask 
        #buffer = 30

        year = ee.Date(self.endDate).get('year') 
        masksHandler = Masks(geometry,masks)
        masksHandler.calculateCombinedMask() # combined mask does not include aspects
        self.sentinel1 = self.sentinel1.map(algorithm = masksHandler.updateCombinedMask)
        
        self.VVAsc     = self.sentinel1.filter(ee.Filter.eq('orbitProperties_pass','ASCENDING' )) \
                                                        .select('VV') \
                                                        .map(filterSpeckles3x3) \
                                                        .map(algorithm = self.renameVVAsc)
        self.VHAsc     = self.sentinel1.filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING' )) \
                                                        .select('VH') \
                                                        .map(filterSpeckles3x3) \
                                                        .map(algorithm = self.renameVHAsc)
        self.VVDes     = self.sentinel1.filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING')) \
                                                        .select('VV') \
                                                        .map(filterSpeckles3x3) \
                                                        .map(algorithm = self.renameVVDes)
        self.VHDes     = self.sentinel1.filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING')).select('VH') \
                                                        .map(filterSpeckles3x3) \
                                                        .map(algorithm = self.renameVHDes)
        self.tmpCol    = None
        self.tmpyear   = 0

        if(applyAspects):
            masksHandlerAscAsp = Masks(geometry,{'aspectAsc':0})
            masksHandlerDesAsp = Masks(geometry,{'aspectDes':0})
            masksHandlerAscAsp.calculateCombinedMask() 
            masksHandlerDesAsp.calculateCombinedMask() 
            self.VVAsc = self.VVAsc.map(algorithm = masksHandlerAscAsp.updateAscMask)
            self.VHAsc = self.VHAsc.map(algorithm = masksHandlerAscAsp.updateAscMask) 
            self.VVDes = self.VVDes.map(algorithm = masksHandlerDesAsp.updateDesMask) 
            self.VHDes = self.VHDes.map(algorithm = masksHandlerDesAsp.updateDesMask)

        years  = [2017]
        months = list(range(1,13))
        #self.VHDes = monthly_Avg(self.VHDes,years,months)
        #self.VHDes     = byMonth(self.VHDes)
        #self.byMonthVHDesVHDes()

    def getVVAsc(self):
        return self.VVAsc

    def getVHAsc(self):
        return self.VHAsc

    def getVVDes(self):
        return self.VVDes

    def getCollectionToBands(self):
        VHAscBands = self.VHAsc.toBands()
        VVAscBands = self.VVAsc.toBands()
        VHDesBands = self.VHDes.toBands()
        VVDesBands = self.VVDes.toBands()
        return VHAscBands.addBands(VVAscBands).addBands(VHDesBands).addBands(VVDesBands)
    
    def getCollectionToBandsAsc(self):
        VHAscBands = self.VHAsc.toBands()
        VVAscBands = self.VVAsc.toBands()
        return VHAscBands.addBands(VVAscBands)
    
    def getCollectionToBandsDes(self):
        VHDesBands = self.VHDes.toBands()
        VVDesBands = self.VVDes.toBands()
        return VHDesBands.addBands(VVDesBands)



    def getVHDes(self):
        return self.VHDes 
    
    def getVVAscMedian(self):
        return self.VVAsc.median()

    def getVHAscMedian(self):
        return self.VHAsc.median()

    def getVVDesMedian(self):
        return self.VVDes.median()

    def getVHDesMedian(self):
        return self.VHDes.median()
    
    
    def getAveOfMonthVHDes(self,m): 
        return  self.VHDes.filter(ee.Filter.calendarRange(m, m, 'month')) #\
                  #  .mean() \
                   # .set('month', m) 

    def byMonthVHDesVHDes(self,i_year,col):
        startDate = ee.Date.fromYMD(i_year, 1, 1)
        endDate = startDate.advance(1, 'year')
        tmpCol = col.filter(ee.Filter.date(startDate, endDate))
        return  ee.ImageCollection.fromImages(ee.List([
        (tmpCol.filter(ee.Filter.calendarRange( 1,  1, 'month')).mean().set('month', 1)),
        (tmpCol.filter(ee.Filter.calendarRange( 2,  2, 'month')).mean().set('month', 2)),
        (tmpCol.filter(ee.Filter.calendarRange( 3,  3, 'month')).mean().set('month', 3)),
        (tmpCol.filter(ee.Filter.calendarRange( 4,  4, 'month')).mean().set('month', 4)),
        (tmpCol.filter(ee.Filter.calendarRange( 5,  5, 'month')).mean().set('month', 5)),
        (tmpCol.filter(ee.Filter.calendarRange( 6,  6, 'month')).mean().set('month', 6)),
        (tmpCol.filter(ee.Filter.calendarRange( 7,  7, 'month')).mean().set('month', 7)),
        (tmpCol.filter(ee.Filter.calendarRange( 8,  8, 'month')).mean().set('month', 8)),
        (tmpCol.filter(ee.Filter.calendarRange( 9,  9, 'month')).mean().set('month', 9)),
        (tmpCol.filter(ee.Filter.calendarRange(10, 10, 'month')).mean().set('month',10)),
        (tmpCol.filter(ee.Filter.calendarRange(11, 11, 'month')).mean().set('month',11)),
        (tmpCol.filter(ee.Filter.calendarRange(12, 12, 'month')).mean().set('month',12))]))
    
    def byMonth(self,i_year):
        self.VHAsc = self.byMonthVHDesVHDes(i_year,self.VHAsc)
        self.VVAsc = self.byMonthVHDesVHDes(i_year,self.VVAsc)
        self.VHDes = self.byMonthVHDesVHDes(i_year,self.VHDes)
        self.VVDes = self.byMonthVHDesVHDes(i_year,self.VVDes)
                    
    # method that removed a given period from the dataset
    def removePeriod(self,startDate, endDate):
        badDataFilter = ee.Filter.date(startDate,endDate)
        self.VHAsc = self.VHAsc.filter(badDataFilter.Not())
        self.VVAsc = self.VVAsc.filter(badDataFilter.Not())
        self.VHDes = self.VHDes.filter(badDataFilter.Not())
        self.VVDes = self.VVDes.filter(badDataFilter.Not())
        print("Period from ", startDate, " to ", endDate, " removed")