# -*- coding: utf-8 -*-

from flickrapi import FlickrAPI

SIZES = {
    'square': 's',
    'thumb': 't',
    'small': 'm',
    'medium': '',
    'extended': 'z',
    'big': 'b'
}

def set_cridentials(api_key, user_id):
    global USER_ID
    USER_ID = user_id
    global flickr
    flickr = FlickrAPI(api_key, cache=True)

class Photo(object):
    """flickr photo object"""

    def __init__(self, id, **kwargs):
        self.id = id
        if kwargs:
            for name, value in kwargs.iteritems():
                setattr(self, name, value)
            for size in SIZES:
                setattr(self, size, self._make_url(size))
        else:
            self._fetch_info()

    def _make_url(self, size):
        if size == 'medium':
            suffix = ''
        else:
            suffix = '_%s' % SIZES[size]
        return 'http://farm%s.staticflickr.com/%s/%s_%s%s.jpg' % (self.farm,
                                                                  self.server,
                                                                  self.id,
                                                                  self.secret,
                                                                  suffix)

    def _fetch_info(self):
        info = flickr.photos_getInfo(photo_id=self.id)[0]
        self.title = info[1].text
        self.description = info[1].text
        sizes = flickr.photos_getSizes(photo_id=self.id)[0]
        self.square = sizes[0].attrib['source']
        self.thumb = sizes[1].attrib['source']
        self.small = sizes[2].attrib['source']
        self.medium = sizes[4].attrib['source']

class Photoset(object):
    """The flickr photoset"""

    def __init__(self, id, for_json=False, **kwargs):
        self.id = id
        self.items = []
        if kwargs:
            for name, value in kwargs.iteritems():
                setattr(self, name, value)
            self.thumb = Photo(id=self.primary, farm=self.farm, server=self.server,
                               secret=self.secret)
            if for_json:
                self.thumb = self.thumb.__dict__
        else:
            self._fetch_info()


    def __iter__(self):
        for item in self.items:
            yield item

    def __getitem__(self, num):
        return self.items[num]

    def __len__(self):
        return len(self.items)

    def _fetch_info(self, for_json):
        info = flickr.photosets_getInfo(photoset_id=self.id)[0]
        self.title = info[0].text
        if info[1].text is not None:
            self.description = info[1].text
        photo_items = flickr.photosets_getPhotos(photoset_id=self.id)[0]
        for item in photo_items:
            if item.attrib['isprimary'] == '1':
                primary = Photo(**item.attrib)
                if for_json:
                    primary = Photo(**item.attrib).__dict__
                self.primary = primary
            photo = Photo(**item.attrib)
            if for_json:
                photo = photo.__dict__
            self.items.append(photo)
        sets = Photoset.fetch_all()
        for index, photoset in enumerate(sets):
            if photoset.id == self.id:
                self.previous = sets[index-1]
                try:
                    self.next = sets[index+1]
                except IndexError, error:
                    self.next = sets[0]

    @classmethod
    def fetch_all(cls, for_json=False):
        photoset_items = flickr.photosets_getList(user_id=USER_ID)[0]
        photosets = []
        for item in photoset_items:
            photoset = Photoset(for_json=for_json, **item.attrib)
            photoset.title = item[0].text
            photoset.description = item[1].text
            if for_json:
                photoset = photoset.__dict__
            photosets.append(photoset)
        return photosets