# Tagging system API

Сервис реализующий api сервиса теггирования фотографий.  

## Routes
      /image: 
          post: загрузка фото 
              params: {"name": <image_file_name>}
              body: <image_file_bytes>
          get: получение всей информации о фото
              params: {"image_id": <image_id>}
      
      /images: 
          post: pagination по всем фото
              params: {"page": <page>, "size": <page_size>}
              response: {
                  "count": <all_images_count>, 
                  "images": [
                      {
                          "id": <image_id>, 
                          "name": <image_name>, 
                          "source_path": <minio_path>, 
                          "tags": [
                              {"id": <tag_id>, "name": <tag_name>}
                              ...
                          ]
                      }
                      ...
                  ]
              }
             
      /images/search: 
          post - pagination по результатам запроса поиска по тегам одного из двух типов (any, all)
              params: {"page": <page>, "size": <page_size>, "tags": <array_of_tag_ids>, "type": "any"|"all"}
              response: {
                  "count": <matched_images_count>, 
                  "images": [
                      {
                          "id": <image_id>, 
                          "name": <image_name>, 
                          "source_path": <minio_path>, 
                          "tags": [
                              {"id": <tag_id>, "name": <tag_name>}
                              ...
                          ]
                      }
                      ...
                  ]
              }
              
      /image/delete: 
          post - удаление изображения
              params: {"image_id": <image_id>}
      
      /tag: 
          post - создание тега
              params: {"name": <tag_ru_name>, "text": <tag_eng_description>, "group_id": <group_id>, "binary": True|False}
              response: {"tag_id": <new_tag_id>}
          get - получение всей информации о теге
              params: {"tag_id": <tag_id>}
              response: {
                  "id": <tag_id>,
                  "name": <tag_name>,
                  "text": <tag_eng_description>,
                  "latent_space": <tag_latent_space>
              }
                
      /tag/delete: 
          post - удаление тега
              params: {"tag_id": <tag_id>}
              
      /tag_group: 
          post - создание группы тегов
              params: {
                  "name": <tag_group_name>,
                  "binary": True|False,
              }
              response: {"group_id": <new_tag_group_id>}
          get - получение всей информации о группе тегов
              params: {"tag_group_id": <tag_group_id>}
              response: {
                  "group": {
                      "id": <tag_group_id>,
                      "name": <tag_group_name>,
                      "binary": True|False
                  },
                  "tags": [
                      {"id": <tag_id>, "name": <tag_name>, "text": <tag_eng_description>, "latent_space": <tag_latent_space>}
                      ...
                  ]
              }
      
      /tag_groups: 
          get - получение всей информации о всех тегах   
              response: [{
                  "group": {
                      "id": <tag_group_id>,
                      "name": <tag_group_name>,
                      "binary": True|False
                  }, 
                  "tags": [
                      {"id": <tag_id>, "name": <tag_name>, "text": <tag_eng_description>, "latent_space": <tag_latent_space>}
                      ...
                  }
                  ...
              ]
              
              
