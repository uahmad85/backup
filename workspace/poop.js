curl -XPOST localhost:9200/close5-uat -d '{

    "user":{

    "properties":{

        "createdAt":{

            "type":"date",

                "format":"dateOptionalTime"

        },

        "email":{

            "type":"string",

                "index":"not_analyzed"

        },

        "facebookId":{

            "type":"string"

        },

        "location":{

            "type":"geo_point",

                "doc_values":true,

                "fielddata":{

                "format":"doc_values"

            },

            "lat_lon":true,

                "geohash":true,

                "geohash_prefix":true,

                "geohash_precision":6

        },

        "name":{

            "properties":{

                "first":{

                    "type":"string"

                },

                "full":{

                    "type":"string"

                },

                "last":{

                    "type":"string"

                }

            }

        },

        "name.full":{

            "type":"string",

                "index":"not_analyzed"

        },

        "photo":{

            "type":"string",

                "index":"not_analyzed"

        },

        "pushToken":{

            "type":"string",

                "index":"not_analyzed"

        },

        "selling":{

            "type":"string",

                "index":"not_analyzed"

        },

        "sold":{

            "type":"string"

        },

        "unlisted":{

            "type":"string",

                "index":"not_analyzed"

        },

        "vanity":{

            "type":"string",

                "index":"not_analyzed"

        }

    }

},

    "item":{

    "_parent":{

        "type":"user"

    },

    "_routing":{

        "required":true

    },

    "properties":{

        "buyerId":{

            "type":"string",

                "index":"not_analyzed"

        },

        "category":{

            "type":"string"

        },

        "createdAt":{

            "type":"date",

                "format":"dateOptionalTime"

        },

        "description":{

            "type":"string",

                "analyzer":"keyword_search"

        },

        "featured":{

            "type":"boolean"

        },

        "live":{

            "type":"boolean"

        },

        "location":{

            "type":"geo_point",

                "doc_values":true,

                "fielddata":{

                "format":"doc_values"

            },

            "lat_lon":true,

                "geohash":true,

                "geohash_prefix":true,

                "geohash_precision":6

        },

        "price":{

            "type":"long"

        },

        "removed":{

            "type":"boolean"

        },

        "soldAt":{

            "type":"date",

                "format":"dateOptionalTime"

        },

        "status":{

            "type":"string",

                "index":"not_analyzed"

        },

        "updatedAt":{

            "type":"date",

                "format":"dateOptionalTime"

        },

        "userId":{

            "type":"string",

                "index":"not_analyzed"

        },

        "watchers":{

            "type":"string",

                "index":"not_analyzed"

        }

    }

}}'