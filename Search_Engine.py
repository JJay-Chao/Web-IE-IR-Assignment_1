import json
from elasticsearch import Elasticsearch, helpers

class Search_Engine(object):

    def __init__(self):
        self.Dcard_QA_mapping = {
            'properties': {
                'id': {
                    'type': 'text'
                },
                'title': {
                    'type': 'text'
                },
                'content': {
                    'type': 'text'
                },
                'topics': {
                    'type': 'text'
                },
                'createdAt': {
                    'type': 'text'
                },
                'updatedAt': {
                    'type': 'text'
                },
                'commentCount': {
                    'type': 'integer'
                },
                'likeCount': {
                    'type': 'integer'
                },
                'forumName': {
                    'type': 'text'
                },
                'school': {
                    'type': 'text'
                },
                'department': {
                    'type': 'text'
                },
                'gender': {
                    'type': 'text'
                },
                'comments': {
                    'type': 'text'
                },
                'comments_likeCount': {
                    'type': 'text'
                }
            }
        }




    def read_data(self):
        with open('Database/健身.json', 'r') as f:
            for line in f:
                d = eval(line.strip())
                d = json.dumps(d)
                d = json.loads(d)
                comment_list = d.pop('Comments')
                comment_content_new = ""
                comment_likeCount_new = ""
                segmentation = '<eos>'

                topics = d.pop('topics')
                topics_string = ''
                for topic in topics:
                    topics_string += topic
                    topics_string += segmentation

                d['topics'] = topics_string

                for comment in comment_list:
                    comment_content_new += comment['content']
                    comment_content_new += segmentation

                    comment_likeCount_new += str(comment['likeCount'])
                    comment_likeCount_new += segmentation

                d['comments'] = comment_content_new
                d['comments_likeCount'] = comment_likeCount_new

                yield d


    def load2ES(self):
        INDEX_NAME = 'dcard_qa'
        DOC_TYPE = 'one_to_one'
        es = Elasticsearch()
        if not es.indices.exists(index=INDEX_NAME):
            es.indices.create(index=INDEX_NAME)

        print('Index Created!')
        if not es.indices.exists_type(index=INDEX_NAME, doc_type=DOC_TYPE):
            es.indices.put_mapping(index=INDEX_NAME, doc_type=DOC_TYPE, body=self.Dcard_QA_mapping)

        print('Mappings Created!')

        success, _ = helpers.bulk(es, self.read_data(), index=INDEX_NAME, doc_type=DOC_TYPE, ignore=400)
        print('success:', success)


    def query(self, target):
        es = Elasticsearch()
        INDEX_NAME = 'dcard_qa'
        DOC_TYPE = 'one_to_one'

        query_mapping_1 = {
            "query": {
                "match": {"topics": target}
            },
            "size": 5
        }

        query_mapping_2 = {
            "query": {
                "match": {"title": target}
            },
            "size": 5
        }

        query_mapping_3 = {
            "query": {
                "match": {"content": target}
            },
            "size": 5
        }

        res_1 = es.search(index=INDEX_NAME, doc_type=DOC_TYPE, body=query_mapping_1)
        res_2 = es.search(index=INDEX_NAME, doc_type=DOC_TYPE, body=query_mapping_2)
        res_3 = es.search(index=INDEX_NAME, doc_type=DOC_TYPE, body=query_mapping_3)
        Result_List = []
        check_same = []
        for result in res_1['hits']['hits']:
            if result['_source']['id'] not in check_same:
                Result_List.append(result)
                check_same.append(result['_source']['id'])

        for result in res_2['hits']['hits']:
            if result['_source']['id'] not in check_same:
                Result_List.append(result)
                check_same.append(result['_source']['id'])

        for result in res_3['hits']['hits']:
            if result['_source']['id'] not in check_same:
                Result_List.append(result)
                check_same.append(result['_source']['id'])

        new_Result_List = sorted(Result_List, key=lambda k: k['_score'], reverse=True)
        Result_List = [dict['_source'] for dict in new_Result_List]



        return Result_List


    def delete(self):
        INDEX_NAME = 'dcard_qa'
        es = Elasticsearch()
        if es.indices.exists(INDEX_NAME):
            es.indices.delete(INDEX_NAME)
