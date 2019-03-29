import requests
import logging
import json

class Dcard(object):

    def __init__(self, API_ROOT, FORUMS, POSTS, headers):
        self.API_ROOT = API_ROOT
        self.FORUMS = FORUMS
        self.POSTS = POSTS
        self.headers = headers

    def get(self, url, headers, verbose=False):
        response = requests.get(url, headers=headers, verify=False)
        if verbose:
            logging.info(response.url)

        try:
            json_data = json.loads(response.text)
        except ValueError:
            return 'Error'

        return json_data


    def filter_general(self, forums):
        for forum in forums:
            if not forum['isSchool']:
                yield forum


    def get_forums(self, headers):
        url = '{api_root}/{api_forums}'.format(api_root=self.API_ROOT, api_forums=self.FORUMS)
        forums = self.get(url, headers, verbose=False)

        return forums


    def get_post_metas(self, forum, params):
        before_tag = ''
        before_id = ''
        if 'before' in params:
            before_tag = 'before='
            before_id = str(params['before'])

        url = '{api_root}/{api_forums}/{forum}/{api_posts}?{popular}&{limit}&{before}'.format(
            api_root=self.API_ROOT,
            api_forums=self.FORUMS,
            api_posts=self.POSTS,
            popular='popular='+params['popular'],
            limit='limit='+params['limit'],
            before=before_tag+before_id,
            forum=forum
        )
        article_metas = self.get(url, headers=self.headers, verbose=False)

        return article_metas


    def get_post_ids(self, forum, pages=3):
        '''
            為了一次取的更多頁的文章 (可以把一次 request 取得 30 筆，視作取得一頁)
            使用此 method 將 `get_post_metas` 做包裝，提供一次抓取多頁文章資訊，
            且通常是為了之後用途而抓取 {文章編號}。
        '''
        params = {
                   'popular': 'false',
                   'limit': '100'
                 }
        ids = []
        for i in range(pages):
            metas = self.get_post_metas(forum, params)
            ids += [e['id'] for e in metas]
            params['before'] = ids[-1]
            print('Collecting page {page_num}'.format(page_num=str(i+1)))
        return ids


    def get_post_content(self, post_meta):
        post_url = '{api_root}/{api_posts}/{post_id}'.format(
            api_root=self.API_ROOT,
            api_posts=self.POSTS,
            post_id=post_meta
        )
        links_url = '{post_url}/links'.format(post_url=post_url)
        comments_url = '{post_url}/comments'.format(post_url=post_url)
        params = {}
        content = self.get(post_url, headers=self.headers, verbose=False)
        if content == 'Error':
            return 'Error'

        comments = []

        while True:
            _comments = self.get(comments_url, headers=self.headers, verbose=True)
            if _comments == 'Error':
                return 'Error'

            if len(_comments) == 0:
                break

            comments += _comments
            try:
                params['after'] = comments[-1]['floor']
            except:
                return {
                    'content': content,
                    'comments': comments
                }

            comments_url = '{post_url}/comments?{after}'.format(post_url=post_url, after='after='+str(params['after']))

        return {
            'content': content,
            'comments': comments
        }


    def Forum_Content_Process(self, Content_dict):
        '''
        id, title, content, createdAt, updatedAt, commentCount, likeCount, forumCount, school, department, gender
        '''
        Forum_Content = {}
        if 'id' in Content_dict:
            Forum_Content['id'] = Content_dict['id']
        else:
            Forum_Content['id'] = 'unknown'

        if 'title' in Content_dict:
            Forum_Content['title'] = Content_dict['title']
        else:
            Forum_Content['title'] = 'unknown'

        if 'content' in Content_dict:
            Forum_Content['content'] = Content_dict['content']
        else:
            Forum_Content['content'] = 'unknown'

        if 'topics' in Content_dict:
            Forum_Content['topics'] = Content_dict['topics']
        else:
            Forum_Content['topics'] = 'unknown'

        if 'createdAt' in Content_dict:
            Forum_Content['createdAt'] = Content_dict['createdAt']
        else:
            Forum_Content['createdAt'] = 'unknown'

        if 'updatedAt' in Content_dict:
            Forum_Content['updatedAt'] = Content_dict['updatedAt']
        else:
            Forum_Content['updatedAt'] = 'unknown'

        if 'commentCount' in Content_dict:
            Forum_Content['commentCount'] = Content_dict['commentCount']
        else:
            Forum_Content['commentCount'] = 'unknown'

        if 'likeCount' in Content_dict:
            Forum_Content['likeCount'] = Content_dict['likeCount']
        else:
            Forum_Content['likeCount'] = 'unknown'

        if 'forumName' in Content_dict:
            Forum_Content['forumName'] = Content_dict['forumName']
        else:
            Forum_Content['forumName'] = 'unknown'

        if 'school' in Content_dict:
            Forum_Content['school'] = Content_dict['school']
        else:
            Forum_Content['school'] = 'unknown'

        if 'department' in Content_dict:
            Forum_Content['department'] = Content_dict['department']
        else:
            Forum_Content['department'] = 'unknown'

        if 'gender' in Content_dict:
            Forum_Content['gender'] = Content_dict['gender']
        else:
            Forum_Content['gender'] = 'unknown'

        Forum_Content['Comments'] = []

        return Forum_Content



    def Forum_Comment_Process(self, Comment_dict):
        '''
        postId, createdAt, updatedAt, floor, content, likeCount, gender, school, department
        '''
        Forum_Comment = {}
        if 'postId' in Comment_dict:
            Forum_Comment['postId'] = Comment_dict['postId']
        else:
            Forum_Comment['postId'] = 'unknown'

        if 'createdAt' in Comment_dict:
            Forum_Comment['createdAt'] = Comment_dict['createdAt']
        else:
            Forum_Comment['createdAt'] = 'unknown'

        if 'updatedAt' in Comment_dict:
            Forum_Comment['updatedAt'] = Comment_dict['updatedAt']
        else:
            Forum_Comment['updatedAt'] = 'unknown'

        if 'floor' in Comment_dict:
            Forum_Comment['floor'] = Comment_dict['floor']
        else:
            Forum_Comment['floor'] = 'unknown'

        if 'content' in Comment_dict:
            Forum_Comment['content'] = Comment_dict['content']
        else:
            Forum_Comment['content'] = 'unknown'

        if 'likeCount' in Comment_dict:
            Forum_Comment['likeCount'] = Comment_dict['likeCount']
        else:
            Forum_Comment['likeCount'] = 'unknown'

        if 'gender' in Comment_dict:
            Forum_Comment['gender'] = Comment_dict['gender']
        else:
            Forum_Comment['gender'] = 'unknown'

        if 'school' in Comment_dict:
            Forum_Comment['school'] = Comment_dict['school']
        else:
            Forum_Comment['school'] = 'unknown'

        if 'department' in Comment_dict:
            Forum_Comment['department'] = Comment_dict['department']
        else:
            Forum_Comment['department'] = 'unknown'

        return Forum_Comment


    def All_Forums(self):
        Forums = {}
        Dcard_forums = self.get_forums(self.headers)
        for line in Dcard_forums:
            board_name = line['alias']
            forum_name = line['name']
            Forums[forum_name] = board_name

        return Forums


    def Dcard_Scraping(self, Forums, forum_name, pages):

        print('Loading data...')

        ids = self.get_post_ids(Forums[forum_name], pages=pages)

        #Content
        Dcard_Content_List = []
        Dcard_Content_Forum = ''

        print('Processing Content & Comment...')

        id_count=0
        for id in ids:
            id_count += 1
            if id_count%100 == 0:
                print('Processing page {page_num}'.format(page_num=str(int(id_count/100))))

            Dcard_Mass = self.get_post_content(id)
            if Dcard_Mass == 'Error':
                continue

            Dcard_Content = self.Forum_Content_Process(Dcard_Mass['content'])
            Dcard_Content_Forum = Dcard_Content['forumName']
            Dcard_Content_List.append(Dcard_Content)
            ##print('-----文章-----')
            ##for key in Dcard_Content.keys():
                ##print(Dcard_Content[key])
            ##print('-----評論-----')
            for Dcard_Comment in Dcard_Mass['comments']:
                Dcard_Comment = self.Forum_Comment_Process(Dcard_Comment)
                Dcard_Content_List[-1]['Comments'].append(Dcard_Comment)
                ##for key in Dcard_Comment.keys():
                ##    print(Dcard_Comment[key])
                ##print('---分隔線---')

        print('Saving json file...')
        #Dcard write json
        with open('Database/{FileName}.json'.format(FileName=Dcard_Content_Forum), 'w') as f:
            for element in Dcard_Content_List:
                json.dump(element, f, ensure_ascii=False)
                f.write('\n')


        print('{FileName} Finished...'.format(FileName=Dcard_Content_Forum))
        print('\n')
