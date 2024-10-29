import ee
from plottosat.utils import filterSpeckles, addBuffer, addBufferRename

class Masks:
    def __init__(self, geometry, masks):
        self.gswBuffer = -1
        self.lmaskBuffer = -1
        self.forestMaskBuffer = -1
        self.forestMapStartDate = ""
        self.forestMapEndDate = ""
        self.aspectDesBuffer = -1
        self.aspectAscBuffer = -1
        self.forestYear = -1
        # aspects buffer will be 0 and not applied
        if(masks!={}):
            if ('gsw' in masks):
                self.gswBuffer = int(masks['gsw'])

            if ('lmask' in masks):
                self.lmaskBuffer = int(masks['lmask'])

            if ('aspectDes' in masks):
                self.aspectDesBuffer = int(masks['aspectDes'])

            if ('aspectAsc' in masks):
                self.aspectAscBuffer = int(masks['aspectAsc'])

            if ('forestMask' in masks):
                tmp            = masks['forestMask']['buffer'   ]
                self.startDate = masks['forestMask']['startDate']
                self.endDate   = masks['forestMask']['endDate'  ]
                self.forestMaskBuffer = tmp
                self.forestMapStartDate = self.startDate
                self.forestMapEndDate = self.endDate 
                

           
        self.dem = ee.Image('NASA/NASADEM_HGT/001').select('elevation').clip(geometry)
        self.aspect = ee.Terrain.aspect(self.dem)
       
        self.asc = (self.aspect.gt(202.5).And(self.aspect.lt(337.5)))
        self.asc = filterSpeckles(self.asc,5,'circle')

        self.des = (self.aspect.gt(22.5).And(self.aspect.lt(157.5)))
        self.des = filterSpeckles(self.des,5,'circle')
        
        # load ground surface water
        gsw = ee.Image("JRC/GSW1_4/GlobalSurfaceWater")
        self.occurrence = gsw.select('occurrence')
        # load a land mask
        self.landMask = ee.Image('CGIAR/SRTM90_V4').clip(geometry).mask()
        # Load Global Forest Change Data
        # "The Hansen et al. (2013) Global Forest Change dataset in Earth
        # Engine represents forest change, at 30 meters resolution, globally, between 2000 and 2021."
        # These data are updated annually
        gfc2021 = ee.Image("UMD/hansen/global_forest_change_2022_v1_10").clip(geometry)
        # extract the band that gives me which year was each tree covered area lost
        self.lossYear = gfc2021.select(['lossyear']).clip(geometry)
        self.loss = gfc2021.select(['loss']).clip(geometry)

        self.combinedMask = ee.Image(1).clip(geometry)
        self.isCombineMaskCalculated = False
        self.geometry = geometry

    def updateNoSurfaceWaterMask(self, image):
        if (self.gswBuffer > 0):
            gswMask = addBuffer(
                self.occurrence, self.gswBuffer).unmask(-999).eq(-999)
            return image.updateMask(gswMask)
        else:
            print("WARNING: Water mask not applied. Buffer needs to be > 0")
            return image

    def updateLandMask(self, image):
        if (self.lmaskBuffer > 0):
            lmask = addBuffer(self.landMask, self.lmaskBuffer).add(1)
            return image.updateMask(lmask)
        else:
            print("WARNING: land mask not applied. Buffer needs to be > 0")
            return image

    def updateAscMask(self, image):
        return image.updateMask(self.asc)

    def updateDesMask(self, image):
        return image.updateMask(self.des)

    def updateForestLostMask(self, image):
        year = 2017
        yearNo = year - 2000
        YOI = self.lossYear.where(self.lossYear.gt(yearNo), 0)
        result = YOI.where(YOI.gt(0), 1)
        resultUnmasked = result.unmask(0)
        return image.updateMask(addBufferRename(result, self.forestMaskBuffer,"forestLost200017").unmask(-999).eq(-999))

    def getAscAspects(self):
        return self.asc

    def getDesAspects(self):
        return self.des

    def getAspects(self):
        return self.aspect

    # @brief method that merges land surface and ocean/sea water into a single mask
    # @brief buffer amount of meters to be added around the water areas
    # @return the land mask of does not contain surface water
    def getNoSurfaceWaterMask(self, buffer):
        # Load a map containing the global surface water
        return addBufferRename(self.occurrence, buffer,"gwmBuffered").unmask(-999).eq(-999)

    # method that return land mask
    # buffer amount of meters to be added around the water areas
    # @return the land mask of does not contain surface water
    def getlandMask(self, buffer):
        return addBufferRename(self.landMask, buffer,"landMaskBuffered ").add(1)

    def getForestLostMask(self, startdate, enddate, buffer):
        startyear = ee.Date(startdate).get('year')
        endyear = ee.Date(enddate).get('year')
        startyearNo = startyear.subtract(2000)
        endyearNo = endyear.subtract(2000)

        YOI = self.lossYear.where(self.lossYear.gt(endyearNo), -1)
        YOI = YOI.where(YOI.lt(startyearNo), 0)
        YOI = YOI.where(YOI.gt(startyearNo), 1)
        # buffer is required to clear previous history before unmasking
        return addBufferRename(YOI, buffer,"forestLost").unmask(-999).eq(-999)

    # method that merges land surface and ocean/sea water into a single mask
    # buffer amount of meters to be added around the water areas
    # @return the land mask of does not contain surface water
    def getNoSurfaceWaterMaskNoBuffer(self):
        # Load a map containing the global surface water
        return self.occurrence.unmask(-999).eq(-999)

    # method that return land mask
    # buffer amount of meters to be added around the water areas
    # @return the land mask of does not contain surface water
    def getlandMaskNoBuffer(self):
        return self.landMask.add(1)

    # Method that create a composite mask according to the input provided in the constructors

    def calculateCombinedMask(self):
        self.combinedMask = ee.Image(1).clip(self.geometry)

        if (self.gswBuffer > 0):
            self.combinedMask = self.combinedMask.And(
                self.getNoSurfaceWaterMask(self.gswBuffer))

        if (self.lmaskBuffer > 0):
            self.combinedMask = self.combinedMask.And(
                self.getlandMask(self.lmaskBuffer))

        if (self.forestMaskBuffer>0 and self.forestMapStartDate!="" and self.forestMapEndDate!=""):
            self.combinedMask = self.combinedMask.And(self.getForestLostMask( \
                self.forestMapStartDate,self.forestMapEndDate,self.forestMaskBuffer))

        if (self.aspectDesBuffer == 0):
            self.combinedMask = self.combinedMask.And(self.des)

        if (self.aspectAscBuffer == 0):
            self.combinedMask = self.combinedMask.And(self.asc)

        self.isCombineMaskCalculated = True
        return self.combinedMask

    def updateCombinedMask(self, image):
        return image.updateMask(self.combinedMask)

    def exportCombinedMaskToDrive(self, scale, description, folder, projection):
        if (not self.isCombineMaskCalculated):
            self.calculateCombinedMask()
        # else:
        #   combined mask has already been calculated
        # print(self.geometry.getInfo()['coordinates'])

        print("STARTING BATCH SCRIPT FOR EXPORTING FILE")
        task = ee.batch.Export.image.toDrive(**{
            'image': self.combinedMask,
            'description': description,
            'folder': folder,
            # 'crs' : projection,
            'region': self.geometry.getInfo()['coordinates'],
            'scale': scale,
            'maxPixels': 1549491660
        })
        task.start()

        print("***END OF CALLING BATCH SCRIPT")