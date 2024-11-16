
class dataInputBase:
    # """
    # singleton class to handle connection to MongoDB server.
    # """
    # def __new__(cls, **kwargs):
    #     if not hasattr(cls, 'instance'):
    #         cls.instance = super(dataInputBase, cls).__new__(cls)
    #     return cls.instance


    def __init__(self,  jsonConfig: dict, **kwargs):
        print("data input base")
        classTypeName = "base"
        # Try/catch connection to database
        # try:
        #     self.__client = pymongo.MongoClient('localhost', 27017, serverSelectionTimeoutMS=5000)
        #     self.__client.server_info()
        #
        # except pymongo.errors.ServerSelectionTimeoutError as err:
        #     print("Failed to connect to Mongod service")
        #     return
        #
        # self.__db = self.__client['seer']
        # self.collcPdcMpr = self.__db['PDESAF_pdc_mpr_results']


    def addIndependantVar(self, collName, field, binningParam):
        print("addIndependantVar")

    def classType(self):
        print(f'{self.__class__.__name__} class type')
        print(f'{self.classTypeName}')