# *********************************************************
# a_library_02/engine_signals.py

# # *********************************************************
# import threading 
# from django.dispatch import Signal
#   
# # *********************************************************
# geoLocateAddressSignal = Signal()  
# 
# # *********************************************************
# class thread_geoLocateAddress(threading.Thread):  
#     def __init__(self, instance, addressChunkList, request):  
#         self.instance          = instance
#         self.addressChunkList  = addressChunkList
#         self.request           = request
#         threading.Thread.__init__(self)
#         print "+++ thread_geoLocateAddress: started"
#            
#     def run (self):  
#         from a_geoAddress_01.models import a_geoAddress_01
#         self.instance.auto_geoAddress = a_geoAddress_01.geocodeAddress(addressString='', addressChunkList=self.addressChunkList, request=self.request)     
#         self.instance.save(fromThread=True, request=self.request)        # passing fromThread=True through kwargs to avoid infinate recursing when saving from a thread
#         print "+++ thread_geoLocateAddress: finished"
#         
# # *********************************************************
# def process_geoLocateAddressSignal(sender, instance, addressChunkList, request, signal, *args, **kwargs):  
#     thread_geoLocateAddress(instance, addressChunkList, request).start()
