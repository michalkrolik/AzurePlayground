import json, os

src_posts_path = '/home/mike/Desktop/Instagram/python/myenv/candf_com_20240823_withcomments/posts'
tgt_posts_path = '/home/mike/Desktop/C&F_Azure/jsons'
azure_storage = 'https://20240901candf.blob.core.windows.net/instagram/media'

json_files = [filename for filename in os.listdir(src_posts_path) if filename.endswith('.json')]

for json_file in json_files:
    final_json = {}
    comments_merged = {}
    comments_arraycomments_final = []
    with open(f'{src_posts_path}/{json_file}', 'r') as file:
        data = json.load(file)
    
        data_dict = {}
        for k, v in data.items():
            id = k
            data_dict["id"] = id
            for k, v in v.items():
                if k == 'picture':
                    if v:
                        data_dict['media'] = 'photo'
                        data_dict['media_url'] = f'{azure_storage}/'+id+'.jpg'
                elif k == 'video':
                    if v:
                        data_dict['media'] = 'video'
                        data_dict['media_url'] = f'{azure_storage}/'+id+'.mp4'
                elif k == 'comments':
                    if v:
                        comments_array = []
                        for k, v in v.items():
                            comment_id = k
                            comments = {}
                            for k, v in v.items():
                                comments['comment_id'] = comment_id
                                comments[k] = v
                            comments_array.append(comments)
                            data_dict['comments'] = comments_array
                    else:
                        data_dict['comments'] = []
                else:
                    data_dict[k] = v
    
    final_json['id'] = id
    final_json['results'] = data_dict

    with open(f'{tgt_posts_path}/{id}.json', 'w') as json_file:
        json.dump(final_json, json_file)
