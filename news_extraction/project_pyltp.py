
# coding: utf-8

# In[389]:


#测试用例：

valid_sample ="""

据人社部网站消息，25日，人社部信息中心有关负责人解读该《通知》称，今年要在所有地市实现签发应用全国统一标准的电子社保卡，至少1亿人领取电子社保卡，所有地市均开通移动支付服务。

雷先生说，交警部门罚了他16次，他只认了一次，交了一次罚款，拿到法院的判决书后，会前往交警队，要求撤销此前的处罚。
律师：不依法粘贴告知单,有谋取罚款之嫌。
陕西金镝律师事务所律师骆裕德说，这起案件中，交警部门在处理交通违法的程序上存在问题。司机违停了，交警应将处罚单张贴在车上，并告知不服可以行使申请复议和提起诉讼的权利。这既是交警的告知义务，也是司机的知情权利。交警如果这么做了，本案司机何以被短时间内处罚16次后才知晓被罚？程序违法，为罚而罚，没有起到教育的目的。

《韩国前中央日报》称，当前韩国海军陆战队拥有2个师和2个旅，还打算在2021年增设航空团，并从今年开始引进30余架运输直升机和20架攻击直升机。此外，韩军正在研发新型登陆装甲车，比现有AAV-7的速度更快、火力更猛。未来韩国海军陆战队还会配备无人机，“将在东北亚三国中占据优势”。
但韩国网友对“韩国海军陆战队世界第二”的说法不以为然。不少网友留言嘲讽称：“这似乎是韩国海军陆战队争取国防预算的软文”“现在很多韩国海军陆战队员都是戴眼镜、瘦豆芽体型，不知道怎么选拔的”“记者大概是海军陆战队退役的吧”。

"""

test_sample = """

新华社香港8月11日电 香港升旗队总会11日在新界元朗一家中学举行“家在中华”升旗礼，吸引多名市民参与。

习近平先生也说过这是一件重要的事情。

正午时分，艳阳高照。由香港多家中学组成的升旗队伍，护送国旗到学校操场的旗杆下。五星红旗伴随着国歌冉冉升起，气氛庄严。
香港升旗队总会主席周世耀在国旗下致辞时表示，最近香港发生很多不愉快的事件，包括部分人侮辱国旗国徽、挑战“一国两制”原则底线，也分化了香港和内地的同胞。希望通过当天举行升旗活动弘扬正能量，并传递一个重要讯息：香港属于中华民族大家庭。

香港升旗队总会总监许振隆勉励年轻人说，要关心社会，关心国家，希望年轻人以国为荣，为国争光。
活动接近尾声，参与者在中国地图上贴上中国国旗，象征大家共同努力建设国家。最后，全体人员合唱《明天会更好》，为香港送上美好祝愿。

今年15岁的郭紫晴在香港土生土长。她表示，这次升旗礼是特别为香港加油而举行的，希望大家都懂得尊重自己的国家。“看着国旗升起，想到自己在中国这片土地上成长，感到十分自豪。”
“升旗仪式(与以往)一样，但意义却不同。”作为当天升旗队成员之一的高中生赵颖贤说，国旗和国徽代表了一个国家的尊严，不容践踏，很期望当天的活动能向广大市民传达这一信息。

即将升读初三的蒋靖轩认为，近日香港发生连串暴力事件，当天的升旗仪式更显意义，希望香港快快恢复平静，港人都团结起来。


"""


# In[6]:


import os
import jieba
import re
import math
import time
from numpy import linalg as la
from collections import defaultdict
from functools import wraps


# In[7]:


from pyltp import Segmentor
from pyltp import Postagger
from pyltp import Parser
from pyltp import NamedEntityRecognizer
from pyltp import SentenceSplitter


# In[220]:


cws_model_path = '/home/student/project/project-01/luhuibo/learn-NLP-luhuibo/lesson-05-project-01/data/ltp_data_v3.4.0/cws.model'
pos_model_path = '/home/student/project/project-01/luhuibo/learn-NLP-luhuibo/lesson-05-project-01/data/ltp_data_v3.4.0/pos.model'
par_model_path = '/home/student/project/project-01/luhuibo/learn-NLP-luhuibo/lesson-05-project-01/data/ltp_data_v3.4.0/parser.model'
ner_model_path = '/home/student/project/project-01/luhuibo/learn-NLP-luhuibo/lesson-05-project-01/data/ltp_data_v3.4.0/ner.model'

#初始化
segmentor = Segmentor()#分词
postagger = Postagger()#词性标注
recognizer = NamedEntityRecognizer()#命名主体识别
parser = Parser()#依存分析
segmentor.load(cws_model_path)
postagger.load(pos_model_path)  
recognizer.load(ner_model_path)  
parser.load(par_model_path)


# In[10]:


say_words = ['勉励','声称', '地指', '自述', '中称', '阐释', '盛赞', '看着', '断定', '该死', '诋毁', '听见', '深信', '责难', '就让', '直说', '矢口否认', '吹嘘', '一再强调', '质问', '澄清', '提及', '认为', '听说', '答', '叹息', '坦言', '举出', '指摘', '坦承', '赞叹', '简直', '撒谎', '交代', '否认', '责问', '知悉', '赞美', '问候', '反指', '时说', '原谅', '反问', '所言', '回答', '放过', '确信', '忍不住', '哀叹', '问道', '敢讲', '答道', '见过', '脱口而出', '讨厌', '记得', '强调', '为何', '知晓', '明白', '喊道', '争辩', '表明', '问', '问起', '批评', '说', '一脸', '报道', '请问', '诊断', '怒斥', '说道', '记住', '告诉', '称赞', '谈起', '特别强调', '听过', '得悉', '提过', '指控', '获知', '指出', '证实', '说出', '询问', '心里', '提到', '慨叹', '重申', '所指', '写到', '宣称', '透漏', '地称', '发问', '听听', '责怪', '想着', '地用', '他称', '倾诉', '追问', '自叹', '谈到', '直言', '详述', '恳求', '察觉到', '说起', '表达', '说明', '谴责', '斥责', '写道', '说谎', '责备', '得知', '感慨', '叹道', '觉得', '读到', '岂能', '告知', '供称', '辩称', '告诫', '夸奖', '痛斥', '大骂', '咒骂', '发觉', '引用', '指证', '看过', '地问', '并不认为', '相信', '称', '阐述', '详细描述', '倾听', '吗', '报道说', '要说', '所述', '原话', '如是说', '说好', '忘记', '坚信', '指着', '警告', '反驳', '还称', '却说', '断言', '感叹', '问及', '抨击', '揭示', '承认', '谈论', '驳斥', '谈及', '所称', '表示', '坦白', '名言', '听', '问过', '常说', '知道', '察觉', '地说', '透露', '何况', '明确指出', '坚称', '回忆', '叹', '遇见', '自言', '听到', '中说', '严厉批评', '发誓', '所说', '指责', '想见', '阐明', '讲过', '讲出', '痛骂', '看来',':','：']

# In[480]:


def sentence_parser(sentence):
    try:
        words_list = list(segmentor.segment(sentence))
        length = len(words_list)
        for num,word in enumerate(words_list):
            if len(word)>=6:
                word = list(jieba.cut(word))
                if len(word)>=2:
                    del words_list[num]
                    for _ in word :words_list.insert(num - length + 1,_)
        postager_list = postagger.postag(words_list)
        wp = parser.parse(words_list,postager_list) #依存分析
        wp_relation = [w.relation for w in wp]

        subject = []
        subject_notcore = []
        predicate = []
        sentence_object = []

        predicate_number = -1 #默认假定主谓语的下标
        subject_number = -1

        for m,n in enumerate(wp):
            if n.relation=='HED': #确定第一个主谓句
                predicate.append(words_list[m])
                predicate_number = m
            if n.relation=='COO' and n.head in [predicate_number + 1,predicate_number + 2]:
                predicate.append(words_list[m])

        for k, v in enumerate(wp):
            if v.relation=='SBV'and v.head == predicate_number + 1 : 
                subject.append(words_list[k])
                subject_number = k
            if v.relation=='SBV': 
                subject_notcore.append((k,words_list[k]))

        name_all = get_complete_subject(words_list[:m],subject,subject_notcore,words_list,subject_number,predicate_number,wp_relation)

        saying = get_saying(words_list,predicate_number,sentence,wp_relation)

        if type(saying) == tuple:

            predicate.append("：")
            saying = ''.join(saying)

        if name_all:
            if re.findall('\w',''.join(saying)):
                return [name_all,saying,predicate]
            else:
                return [name_all,''.join(predicate),predicate]
        else:
            return [False,False,False]
    except Exception as e:
        with open('error.txt','a') as err:
            err.write(str(e) + 'get_saying\n')
        return 'error'


# In[469]:


#获得主语
def get_complete_subject(text_forward,subject_list,subject_notcore,words_list,subject_number,predicate_number,parser_list):
    try:
        #解决括号主语的问题《》<> “”
        re_match = ["(<.+?>)","(《.+?》)","(“.+?”)"]
        if subject_list:
            for re_match_one in re_match:
                new_subject = re.findall(re_match_one,''.join(text_forward))
                if new_subject:
                   #print(new_subject,subject_list)
                    if subject_list[0] in new_subject[0]:
                        return new_subject
            for i in range(subject_number-1,-1,-1):
                if parser_list[i] =="ATT":
                    subject_list.insert(0,words_list[i])
                else:
                    return ''.join(subject_list)
            return ''.join(subject_list)

        else:

            if subject_notcore:
                subject_notcore_content =defaultdict(list)
                for number,subject_assistant in subject_notcore:
                    subject_notcore_content[number].insert(0,subject_assistant)
                    for i in range(number-1,-1,-1):
                        if parser_list[i] =="ATT":
                            subject_notcore_content[number].insert(0,words_list[i])
                        else:
                            break
                key_core = sorted([_ for _ in subject_notcore_content.keys() if _ < predicate_number],key = lambda x:(x-predicate_number))
                if key_core:
                    if key_core[0] < predicate_number:
                        return ''.join(subject_notcore_content[key_core[0]])
                else:
                    return False
    except Exception as e:
        with open('error.txt','a') as err:
            err.write(str(e) + 'get_complete_subject\n')
        return 'error'

# 获取谓语内容 #text_forward,subject_list,words_list,subject_number,parser_list
def get_saying(words_list,predicate_number,sentence,parser_list):
    try:
        for biaodian in [ "：",":"]:
            if biaodian in sentence:return (sentence[sentence.index(biaodian)+1:],)
            
        if len(parser_list) > (predicate_number+1):
            
            if all(p in ['VOB','wp'] for p in parser_list[predicate_number +1:]):
                return ''.join(words_list[predicate_number+1:]).strip(',').strip('，')
            
            if parser_list[predicate_number+1] in ['RAD','DBL','VOB','COO']:
                return get_saying(words_list,predicate_number+1,sentence,parser_list)

        return ''.join(words_list[predicate_number+1:]).strip(',').strip('，')
    except Exception as e:
        with open('error.txt','a') as err:
            err.write(str(e) + 'get_saying\n')
        return 'error'


# In[498]:


#工具函数
def text_split(text):
    
    return [x for x in SentenceSplitter.split(text) if x]

def get_details(text):
    words_list = list(segmentor.segment(text))
    length = len(words_list)
    for num,word in enumerate(words_list):
        if len(word)>=6:
            word = list(jieba.cut(word))
            if len(word)>=2:
                del words_list[num]
                for _ in word :words_list.insert(num - length + 1,_)
    postaggers = postagger.postag(words_list)
    name_object = recognizer.recognize(words_list, postaggers)
    parser_list = parser.parse(words_list, postaggers)

    """ 
    print("【分词】\n",list(enumerate(words_list)))
    print("【词性】\n",list(enumerate(postaggers)))
    print("【命名实体】\n",list(enumerate(name_object)))
    print("【依存关系】\n",list(enumerate(["%d:%s" % (arc.head, arc.relation) for arc in parser_list])))
    """
