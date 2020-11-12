from django.db import models
from pymongo import MongoClient
from django.db.models.signals import pre_delete,post_save,pre_save
from django.dispatch.dispatcher import receiver
from PIL import Image
from PIL.ExifTags import TAGS

uri = "mongodb://root:root@52.188.19.176:27017/?authSource=admin&authMechanism=SCRAM-SHA-256"
client = MongoClient(uri)
mydb = client["clouddatabase"]
mycol = mydb["imagemetadata"]

class ImageSet(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='imgset/', null=True, blank=False)

def getmetadatadict(path):
    retdict = {}
    retdict.update({"imgpath":str(path)})
    image = Image.open(path)
    exifdata = image.getexif()
    for tag_id in exifdata:
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        if isinstance(data, bytes):
            data = data.decode()
        data = str(data)
        tag = str(tag)
        retdict.update({tag:data})
        #print(f"{tag}: {data}")
    #print(retdict)
    return retdict

@receiver(post_save, sender=ImageSet)
def imageset_save(sender, instance, **kwargs):
    metadict = getmetadatadict(instance.image.path)
    #print(metadict)
    x = mycol.insert_one(metadict)

@receiver(pre_delete, sender=ImageSet)
def imageset_delete(sender, instance, **kwargs):
    myquery = { "imgpath":str(instance.image.path)}
    mycol.delete_one(myquery)  
