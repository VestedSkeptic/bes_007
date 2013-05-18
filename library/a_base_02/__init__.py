#### *********************************************************
###class a_base_02_node(standard_models.Model): 
###    __metaclass__ = IntermediateModelBase 
###    
###    # -----------------------------------------------------
###    def update_engine_nodeManager_a(self, parent_content_type, className):
###        from engine_nodeManager_a.models import engine_nodeManager_a
###
###        node_content_type = ContentType.objects.get(app_label=className, model=className.lower())
###        try:
###            instance = engine_nodeManager_a.objects.get(parent=parent_content_type, node=node_content_type)
###        except ObjectDoesNotExist:
###            instance = engine_nodeManager_a.objects.create(parent=parent_content_type, node=node_content_type)
###    
####        instance.count = internalRegisteredClassesDict[className].objects.filter(content_type=parent_content_type).count()
###        instance.count = internalRegisteredClassesDict[className].classObject.objects.filter(content_type=parent_content_type).count()
###        instance.save()        # Not a versioned class therefore don't have to pass request into save()
###
###    # -----------------------------------------------------
###    def save(self, **kwargs):
###        super(a_base_02_node, self).save(**kwargs)
###        self.update_engine_nodeManager_a(self.content_type, self.__class__.__name__)
###
###    # -----------------------------------------------------
###    def delete(self, **kwargs):
###        super(a_base_02_node, self).delete(**kwargs)
###        self.update_engine_nodeManager_a(self.content_type, self.__class__.__name__)



        
##### *********************************************************
####class applicationRestartData(a_base_02): 
#####    name              = standard_models.CharField        (max_length = 100)
#####    parentName        = standard_models.CharField        (max_length = 150, blank = True, null = True)
#####    parent            = standard_models.ForeignKey       ('self', blank = True, null = True)  
#####    ancestorId        = standard_models.IntegerField     (default=0, blank = True, null = True)     
#####    explanation       = standard_models.TextField        (blank = True, null = True)     
#####    count             = standard_models.IntegerField     (default=0)     
####    _dataDict          = standard_models.TextField        (blank = True, null = True)
####    auto_fields       = ['auto_timeStamp'] 
####
####    # -----------------------------------------------------
####    def _get_dataDict(self):
####        returnDict = {}
####        if (self._dataDict): returnDict = cPickle.loads(self._dataDict.encode('ascii'))
####        return returnDict
####    def _set_dataDict(self, xDict):
####        self._dataDict =  cPickle.dumps(xDict)
####    dataDict = property(_get_dataDict, _set_dataDict)