import json
import pandas as pd
import random
from xeger import Xeger


class PlaceHolder:
    def __init__(self, string, types, func=None, pattern=None, values=None):
        assert string.count('$') == len(types)
        self.string = string
        self.types = types
        self.func = func
        self.pattern = pattern
        self.values = values

    def generate(self):
        string = ''
        if self.func is None:
            values = []
            for char in self.string:
                if char == '$':
                    if self.pattern is None:
                        if isinstance(self.values[0], list):
                            tmp_values = random.choice(self.values)
                            values.append(tmp_values[0])
                            string += random.choice(tmp_values)
                        else:
                            values.append(random.choice(self.values))
                            string += values[-1]
                    else:
                        values.append(Xeger().xeger(self.pattern))
                        string += values[-1]
                else:
                    string += char
        else:
            values = self.func()
            idx = 0
            for char in self.string:
                if char == '$':
                    string += values[idx]
                    idx += 1
                else:
                    string += char
        return string, values


def generate_integer():
    return [str(random.randint(1, 30))]


def generate_small_real():
    return [str(round(random.uniform(0, 1), 2))]


def generate_large_real():
    return [str(round(random.uniform(0, 10000), 2))]


def generate_date():
    year = random.randint(2000, 2021)
    month = random.randint(1, 12)
    if month in [1, 3, 5, 7, 8, 10, 12]:
        day = random.randint(1, 31)
    elif month in [4, 6, 9, 11]:
        day = random.randint(1, 30)
    elif (year % 4 == 0 and year % 100 > 0) or year % 400 == 0:
        day = random.randint(1, 29)
    else:
        day = random.randint(1, 28)
    return [f'{year}-{str(month).zfill(2)}-{str(day).zfill(2)}']


def generate_two_dates():
    while 1:
        first_date = generate_date()[0]
        second_date = generate_date()[0]
        if first_date < second_date:
            break
    return [first_date, second_date]


def generate_name():
    last_names = '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏' \
        '陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳'
    male_first_names = ['安邦', '安福', '安歌', '安国', '安和', '安康', '安澜', '安民', '安宁', '安平', '安然', '安顺', '安翔',
        '安晏', '安宜', '安怡', '安易', '安志', '昂然', '昂雄', '宾白', '宾鸿', '宾实', '彬彬', '彬炳', '彬郁', '斌斌', '斌蔚',
        '滨海', '波光', '波鸿', '波峻', '波涛', '博瀚', '博超', '博达', '博厚', '博简', '博明', '博容', '博赡', '博涉', '博实',
        '博涛', '博文', '博学', '博雅', '博延', '博艺', '博易', '博裕', '博远', '才捷', '才良', '才艺', '才英', '才哲', '才俊',
        '成和', '成弘', '成化', '成济', '成礼', '成龙', '成仁', '成双', '成天', '成业', '成益', '成荫', '成周', '承安', '承弼',
        '承德', '承恩', '承福', '承基', '承教', '承平', '承嗣', '承天', '承望', '承宣', '承颜', '承业', '承悦', '承允', '承运',
        '承载', '承泽', '承志', '德本', '德海', '德厚', '德华', '德辉', '德惠', '德容', '德润', '德寿', '德水', '德馨', '德曜',
        '德业', '德义', '德庸', '德佑', '德宇', '德元', '德运', '德泽', '德明', '飞昂', '飞白', '飞飙', '飞掣', '飞尘', '飞沉',
        '飞驰', '飞光', '飞翰', '飞航', '飞翮', '飞鸿', '飞虎', '飞捷', '飞龙', '飞鸾', '飞鸣', '飞鹏', '飞扬', '飞文', '飞翔',
        '飞星', '飞翼', '飞英', '飞宇', '飞羽', '飞雨', '飞语', '飞跃', '飞章', '飞舟', '风华', '丰茂', '丰羽', '刚豪', '刚洁',
        '刚捷', '刚毅', '高昂', '高岑', '高畅', '高超', '高驰', '高达', '高澹', '高飞', '高芬', '高峯', '高歌', '高格', '高寒',
        '高翰', '高杰', '高洁', '高峻', '高朗', '高丽', '高邈', '高旻', '高明', '高爽', '高兴', '高轩', '高雅', '高扬', '高阳',
        '高义', '高谊', '高逸', '高懿', '高原', '高远', '高韵', '高卓', '光赫', '光华', '光辉', '光济', '光霁', '光亮', '光临',
        '光明', '光启', '光熙', '光耀', '光誉', '光远', '国安', '国兴', '国源', '冠宇', '冠玉', '晗昱', '晗日', '涵畅', '涵涤',
        '涵亮', '涵忍', '涵容', '涵润', '涵涵', '涵煦', '涵蓄', '涵衍', '涵意', '涵映', '涵育', '翰采', '翰池', '翰飞', '翰海',
        '翰翮', '翰林', '翰墨', '翰学', '翰音', '瀚玥', '翰藻', '瀚海', '瀚漠', '昊苍', '昊昊', '昊空', '昊乾', '昊穹', '昊然',
        '昊然', '昊天', '昊焱', '昊英', '浩波', '浩博', '浩初', '浩大', '浩宕', '浩荡', '浩歌', '浩广', '浩涆', '浩瀚', '浩浩',
        '浩慨', '浩旷', '浩阔', '浩漫', '浩淼', '浩渺', '浩邈', '浩气', '浩然', '浩穰', '浩壤', '浩思', '浩言', '皓轩', '和蔼',
        '和安', '和璧', '和昶', '和畅', '和风', '和歌', '和光', '和平', '和洽', '和惬', '和顺', '和硕', '和颂', '和泰', '和悌',
        '和通', '和同', '和煦', '和雅', '和宜', '和怡', '和玉', '和裕', '和豫', '和悦', '和韵', '和泽', '和正', '和志', '鹤轩',
        '弘博', '弘大', '弘方', '弘光', '弘和', '弘厚', '弘化', '弘济', '弘阔', '弘亮', '弘量', '弘深', '弘盛', '弘图', '弘伟',
        '弘文', '弘新', '弘雅', '弘扬', '弘业', '弘义', '弘益', '弘毅', '弘懿', '弘致', '弘壮', '宏伯', '宏博', '宏才', '宏畅',
        '宏达', '宏大', '宏放', '宏富', '宏峻', '宏浚', '宏恺', '宏旷', '宏阔', '宏朗', '宏茂', '宏邈', '宏儒', '宏深', '宏胜',
        '宏盛', '宏爽', '宏硕', '宏伟', '宏扬', '宏义', '宏逸', '宏毅', '宏远', '宏壮', '鸿宝', '鸿波', '鸿博', '鸿才', '鸿彩',
        '鸿畅', '鸿畴', '鸿达', '鸿德', '鸿飞', '鸿风', '鸿福', '鸿光', '鸿晖', '鸿朗', '鸿文', '鸿熙', '鸿羲', '鸿禧', '鸿信',
        '鸿轩', '鸿煊', '鸿煊', '鸿雪', '鸿羽', '鸿远', '鸿云', '鸿运', '鸿哲', '鸿祯', '鸿振', '鸿志', '鸿卓', '华奥', '华采',
        '华彩', '华灿', '华藏', '华池', '华翰', '华皓', '华晖', '华辉', '华茂', '华美', '华清', '华荣', '华容', '嘉赐', '嘉德',
        '嘉福', '嘉良', '嘉茂', '嘉木', '嘉慕', '嘉纳', '嘉年', '嘉平', '嘉庆', '嘉荣', '嘉容', '嘉瑞', '嘉胜', '嘉石', '嘉实',
        '嘉树', '嘉澍', '嘉熙', '嘉禧', '嘉祥', '嘉歆', '嘉许', '嘉勋', '嘉言', '嘉谊', '嘉懿', '嘉颖', '嘉佑', '嘉玉', '嘉誉',
        '嘉悦', '嘉运', '嘉泽', '嘉珍', '嘉祯', '嘉志', '嘉致', '坚白', '坚壁', '坚秉', '坚成', '坚诚', '建安', '建白', '建柏',
        '建本', '建弼', '建德', '建华', '建明', '建茗', '建木', '建树', '建同', '建修', '建业', '建义', '建元', '建章', '建中',
        '健柏', '金鑫', '锦程', '瑾瑜', '晋鹏', '经赋', '经亘', '经国', '经略', '经纶', '经纬', '经武', '经业', '经义', '经艺',
        '景澄', '景福', '景焕', '景辉', '景辉', '景龙', '景明', '景山', '景胜', '景铄', '景天', '景同', '景曜', '靖琪', '君昊',
        '君浩', '俊艾', '俊拔', '俊弼', '俊才', '俊材', '俊驰', '俊楚', '俊达', '俊德', '俊发', '俊风', '俊豪', '俊健', '俊杰',
        '俊捷', '俊郎', '俊力', '俊良', '俊迈', '俊茂', '俊美', '俊民', '俊名', '俊明', '俊楠', '俊能', '俊人', '俊爽', '俊悟',
        '俊晤', '俊侠', '俊贤', '俊雄', '俊雅', '俊彦', '俊逸', '俊英', '俊友', '俊语', '俊誉', '俊远', '俊哲', '俊喆', '俊智',
        '峻熙', '季萌', '季同', '开畅', '开诚', '开宇', '开济', '开霁', '开朗', '凯安', '凯唱', '凯定', '凯风', '凯复', '凯歌',
        '凯捷', '凯凯', '凯康', '凯乐', '凯旋', '凯泽', '恺歌', '恺乐', '康安', '康伯', '康成', '康德', '康复', '康健', '康乐',
        '康宁', '康平', '康胜', '康盛', '康时', '康适', '康顺', '康泰', '康裕', '乐安', '乐邦', '乐成', '乐池', '乐和', '乐家',
        '乐康', '乐人', '乐容', '乐山', '乐生', '乐圣', '乐水', '乐天', '乐童', '乐贤', '乐心', '乐欣', '乐逸', '乐意', '乐音',
        '乐咏', '乐游', '乐语', '乐悦', '乐湛', '乐章', '乐正', '乐志', '黎昕', '黎明', '力夫', '力强', '力勤', '力行', '力学',
        '力言', '立诚', '立果', '立人', '立辉', '立轩', '立群', '良奥', '良弼', '良才', '良材', '良策', '良畴', '良工', '良翰',
        '良吉', '良骥', '良俊', '良骏', '良朋', '良平', '良哲', '理群', '理全', '茂才', '茂材', '茂德', '茂典', '茂实', '茂学',
        '茂勋', '茂彦', '敏博', '敏才', '敏达', '敏睿', '敏学', '敏智', '明诚', '明达', '明德', '明辉', '明杰', '明俊', '明朗',
        '明亮', '明旭', '明煦', '明轩', '明远', '明哲', '明喆', '明知', '明志', '明智', '明珠', '朋兴', '朋义', '彭勃', '彭薄',
        '彭彭', '彭魄', '彭越', '彭泽', '彭祖', '鹏程', '鹏池', '鹏飞', '鹏赋', '鹏海', '鹏鲸', '鹏举', '鹏鹍', '鹏鲲', '鹏涛',
        '鹏天', '鹏翼', '鹏云', '鹏运', '濮存', '溥心', '璞玉', '璞瑜', '浦和', '浦泽', '奇略', '奇迈', '奇胜', '奇水', '奇思',
        '奇邃', '奇伟', '奇玮', '奇文', '奇希', '奇逸', '奇正', '奇志', '奇致', '祺福', '祺然', '祺祥', '祺瑞', '琪睿', '庆生',
        '荣轩', '锐达', '锐锋', '锐翰', '锐进', '锐精', '锐立', '锐利', '锐思', '锐逸', '锐意', '锐藻', '锐泽', '锐阵', '锐志',
        '锐智', '睿博', '睿才', '睿诚', '睿慈', '睿聪', '睿达', '睿德', '睿范', '睿广', '睿好', '睿明', '睿识', '睿思', '绍辉',
        '绍钧', '绍祺', '绍元', '升荣', '圣杰', '晟睿', '思聪', '思淼', '思源', '思远', '思博', '斯年', '斯伯', '泰初', '泰和',
        '泰河', '泰鸿', '泰华', '泰宁', '泰平', '泰清', '泰然', '天材', '天成', '天赋', '天干', '天罡', '天工', '天翰', '天和',
        '天华', '天骄', '天空', '天禄', '天路', '天瑞', '天睿', '天逸', '天佑', '天宇', '天元', '天韵', '天泽', '天纵', '同方',
        '同甫', '同光', '同和', '同化', '同济', '巍昂', '巍然', '巍奕', '伟博', '伟毅', '伟才', '伟诚', '伟茂', '伟懋', '伟祺',
        '伟彦', '伟晔', '伟泽', '伟兆', '伟志', '温纶', '温茂', '温书', '温韦', '温文', '温瑜', '文柏', '文昌', '文成', '文德',
        '文栋', '文赋', '文光', '文翰', '文虹', '文华', '文康', '文乐', '文林', '文敏', '文瑞', '文山', '文石', '文星', '文轩',
        '文宣', '文彦', '文曜', '文耀', '文斌', '文彬', '文滨', '向晨', '向笛', '向文', '向明', '向荣', '向阳', '翔宇', '翔飞',
        '项禹', '项明', '晓博', '心水', '心思', '心远', '欣德', '欣嘉', '欣可', '欣然', '欣荣', '欣怡', '欣怿', '欣悦', '新翰',
        '新霁', '新觉', '新立', '新荣', '新知', '信鸿', '信厚', '信鸥', '信然', '信瑞', '兴安', '兴邦', '兴昌', '兴朝', '兴德',
        '兴发', '兴国', '兴怀', '兴平', '兴庆', '兴生', '兴思', '兴腾', '兴旺', '兴为', '兴文', '兴贤', '兴修', '兴学', '兴言',
        '兴业', '兴运', '星波', '星辰', '星驰', '星光', '星海', '星汉', '星河', '星华', '星晖', '星火', '星剑', '星津', '星阑',
        '星纬', '星文', '星宇', '星雨', '星渊', '星洲', '修诚', '修德', '修杰', '修洁', '修谨', '修筠', '修明', '修能', '修平',
        '修齐', '修然', '修为', '修伟', '修文', '修雅', '修永', '修远', '修真', '修竹', '修贤', '旭尧', '炫明', '学博', '学海',
        '学林', '学民', '学名', '学文', '学义', '学真', '雪松', '雪峰', '雪风', '雅昶', '雅畅', '雅达', '雅惠', '雅健', '雅珺',
        '雅逸', '雅懿', '雅志', '炎彬', '阳飙', '阳飇', '阳冰', '阳波', '阳伯', '阳成', '阳德', '阳华', '阳晖', '阳辉', '阳嘉',
        '阳平', '阳秋', '阳荣', '阳舒', '阳朔', '阳文', '阳曦', '阳夏', '阳旭', '阳煦', '阳炎', '阳焱', '阳曜', '阳羽', '阳云',
        '阳泽', '阳州', '烨赫', '烨华', '烨磊', '烨霖', '烨然', '烨烁', '烨伟', '烨烨', '烨熠', '烨煜', '毅然', '逸仙', '逸明',
        '逸春', '宜春', '宜民', '宜年', '宜然', '宜人', '宜修', '意远', '意蕴', '意致', '意智', '熠彤', '懿轩', '英飙', '英博',
        '英才', '英达', '英发', '英范', '英光', '英豪', '英华', '英杰', '英朗', '英锐', '英睿', '英睿', '英韶', '英卫', '英武',
        '英悟', '英勋', '英彦', '英耀', '英奕', '英逸', '英毅', '英哲', '英喆', '英卓', '英资', '英纵', '永怡', '永春', '永安',
        '永昌', '永长', '永丰', '永福', '永嘉', '永康', '永年', '永宁', '永寿', '永思', '永望', '永新', '永言', '永逸', '永元',
        '永贞', '咏德', '咏歌', '咏思', '咏志', '勇男', '勇军', '勇捷', '勇锐', '勇毅', '宇达', '宇航', '宇寰', '宇文', '宇荫',
        '雨伯', '雨华', '雨石', '雨信', '雨星', '雨泽', '玉宸', '玉成', '玉龙', '玉泉', '玉山', '玉石', '玉书', '玉树', '玉堂',
        '玉轩', '玉宇', '玉韵', '玉泽', '煜祺', '元白', '元德', '元化', '元基', '元嘉', '元甲', '元驹', '元凯', '元恺', '元魁',
        '元良', '元亮', '元龙', '元明', '元青', '元思', '元纬', '元武', '元勋', '元正', '元忠', '元洲', '远航', '苑博', '苑杰',
        '越彬', '蕴涵', '蕴和', '蕴藉', '展鹏', '哲瀚', '哲茂', '哲圣', '哲彦', '振海', '振国', '正诚', '正初', '正德', '正浩',
        '正豪', '正平', '正奇', '正青', '正卿', '正文', '正祥', '正信', '正雅', '正阳', '正业', '正谊', '正真', '正志', '志诚',
        '志新', '志勇', '志明', '志国', '志强', '志尚', '志专', '志文', '志行', '志学', '志业', '志义', '志用', '志泽', '致远',
        '智明', '智鑫', '智勇', '智敏', '智志', '智渊', '子安', '子晋', '子民', '子明', '子默', '子墨', '子平', '子琪', '子石',
        '子实', '子真', '子濯', '子昂', '子轩', '子瑜', '自明', '自强', '作人', '自怡', '自珍', '曾琪', '泽宇', '泽语']
    female_first_names = ['安安', '荌荌', '安卉', '安娜', '安妮', '安然', '傲冬', '傲晴', '傲雪', '白雪', '白云', '碧螺', '碧菡',
        '碧玉', '冰蓝', '冰冰', '采绿', '采文', '采萱', '初雪', '春华', '春雪', '丹丹', '丹彤', '丹红', '冬雪', '芳芳', '方方',
        '芳菲', '芳华', '芳馨', '芳泽', '芳馥', '芳懿', '芳茵', '芳蕙', '芳春', '芳洲', '芳蕤', '芳润', '芳荃', '芳林', '芳苓',
        '芳洁', '芳蔼', '飞双', '飞雪', '飞烟', '飞燕', '飞英', '谷雪', '古兰', '古韵', '古香', '歌阑', '歌吹', '歌韵', '歌飞',
        '格菲', '葛菲', '戈雅', '格格', '含烟', '含玉', '涵菡', '晗蕾', '涵韵', '晗玥', '寒凝', '寒香', '寒雁', '和悌', '和美',
        '和怡', '和雅', '和璧', '和玉', '和暖', '红叶', '红豆', '红雪', '红英', '红云', '红旭', '红香', '红艳', '红螺', '虹雨',
        '虹彩', '虹英', '虹颖', '虹影', '怀玉', '慧心', '慧颖', '慧雅', '慧智', '慧美', '慧捷', '慧丽', '慧月', '慧云', '慧俊',
        '慧秀', '慧巧', '慧英', '慧艳', '浩岚', '家美', '家欣', '家馨', '佳悦', '嘉怡', '嘉宝', '嘉惠', '嘉悦', '嘉歆', '嘉美',
        '嘉云', '嘉玉', '嘉丽', '嘉淑', '嘉怡', '嘉懿', '洁玉', '晶滢', '晶辉', '静曼', '静涵', '静逸', '静姝', '静娴', '静婉',
        '静雅', '静慧', '静云', '静安', '静秀', '娟秀', '娟妍', '娟丽', '娟巧', '兰若', '兰蕙', '兰梦', '兰泽', '兰芝', '兰英',
        '兰娜', '岚霏', '岚翠', '岚彩', '乐安', '乐心', '乐悦', '乐容', '乐英', '丽泽', '丽华', '丽雅', '丽芳', '丽佳', '丽姿',
        '丽珠', '丽容', '丽文', '灵秀', '灵韵', '灵慧', '灵卉', '灵萱', '玲玲', '玲珑', '凌波', '凌春', '凌霜', '凌雪', '莉莉',
        '曼蔓', '曼冬', '曼青', '曼容', '曼文', '曼妮', '曼云', '曼衍', '曼丽', '曼语', '曼辞', '曼珠', '曼音', '曼吟', '美丽',
        '美华', '米琪', '梦凡', '梦菲', '梦菡', '梦露', '梦琪', '梦秋', '梦竹', '妙晴', '玛丽', '茉莉', '麦冬', '念文', '凝雪',
        '娜兰', '妮娜', '纳兰', '沛珊', '沛文', '萍韵', '萍雅', '绮玉', '清雅', '清逸', '清华', '清秋', '清馨', '清心', '清韵',
        '清芬', '清涵', '清妍', '清昶', '清怡', '清婉', '清晖', '清绮', '清漪', '清卓', '清懿', '清润', '清俊', '清宁', '清淑',
        '清舒', '清霁', '清佳', '清妙', '庆雪', '晴岚', '晴雪', '晴虹', '晴波', '晴霞', '晴丽', '晴照', '晴画', '蓉蓉', '融雪',
        '如风', '如云', '若云', '若兰', '诗兰', '诗蕾', '诗蕊', '书萱', '淑兰', '舒兰', '舒云', '舒方', '淑华', '思美', '思云',
        '施诗', '天韵', '天心', '天蓝', '听云', '甜恬', '恬美', '恬然', '恬静', '婷美', '婷秀', '宛白', '琬凝', '婉然', '婉仪',
        '婉静', '婉慧', '婉丽', '婉容', '婉秀', '婉清', '婉娜', '雯丽', '雯华', '文茵', '文静', '文君', '文漪', '文丽', '文心',
        '文惠', '文敏', '玟丽', '玟玉', '问筠', '问萍', '惜文', '惜雪', '惜玉', '夏菡', '夏兰', '夏岚', '夏青', '夏彤', '夏旋',
        '霞绮', '霞飞', '霞辉', '霞姝', '霞月', '霞英', '霞雰', '霞影', '霞赩', '霞文', '湘云', '香馨', '向卉', '向彤', '向雪',
        '晓燕', '晓莉', '晓凡', '晓兰', '晓曼', '晓霜', '笑寒', '心语', '心香', '心愫', '心宜', '心怡', '心诺', '心远', '新梅',
        '欣美', '欣然', '欣悦', '欣欣', '欣嘉', '欣荣', '欣愉', '欣可', '欣畅', '欣跃', '欣合', '欣笑', '欣艳', '新蕾', '新雪',
        '新月', '馨香', '馨逸', '馨荣', '馨兰', '馨欣', '秀丽', '秀美', '秀逸', '秀雅', '秀华', '秀兰', '秀颖', '秀隽', '秀曼',
        '秀媛', '秀筠', '秀慧', '秀媚', '秀婉', '秀艾', '秀敏', '秀英', '秀越', '秀竹', '秀妮', '秀洁', '秀艳', '璇玑', '璇子',
        '璇珠', '雪枫', '雪卉', '雪曼', '雪萍', '雪晴', '寻春', '寻绿', '寻芳', '雅宁', '雅琴', '雅容', '雅柔', '雅蕊', '雅彤',
        '雅韵', '雅娴', '雅懿', '雅静', '雅洁', '雅丽', '雅惠', '雅韶', '雅素', '雅爱', '雅美', '雅云', '雅媚', '雅艳', '雅可',
        '艳丽', '艳芳', '艳娇', '艳蕊', '艳卉', '依白', '依然', '依波', '依秋', '依美', '依云', '逸云', '逸美', '逸馨', '倚云',
        '怡然', '怡宁', '以晴', '以蕊', '以彤', '以轩', '忆梅', '忆秋', '忆彤', '忆雪', '英华', '英秀', '英媛', '盈秀', '迎秋',
        '莹玉', '莹华', '莹琇', '颖慧', '颖馨', '颖然', '颖秀', '颖初', '映波', '映寒', '映秋', '幼仪', '幼怡', '幼安', '雨筠',
        '雨竹', '语燕', '语心', '语诗', '悦欣', '悦可', '悦欣', '悦心', '悦爱', '云梦', '云水', '云霞', '云露', '云英', '云岚',
        '云逸', '云臻', '云韶', '云飞', '云蔚', '云亭', '蕴秀', '蕴美', '韵诗', '智美', '智敏', '智纯', '芷若', '芷文', '子珍',
        '子萱', '子怡', '子美', '湛蓝', '湛英', '湛芳']
    sex = random.randint(0, 1)
    return [random.choice(last_names) + (random.choice(male_first_names) if sex == 0 else random.choice(female_first_names))]


def generate_dataset():
    place_holders = {
        '整数': PlaceHolder('$', ['number'], func=generate_integer),
        '小实数': PlaceHolder('$', ['number'], func=generate_small_real),
        '大实数': PlaceHolder('$', ['number'], func=generate_large_real),
        '时间': PlaceHolder('$', ['text'], func=generate_date),
        '时间段': PlaceHolder('$到$', ['text', 'text'], func=generate_two_dates),
        '医疗就诊ID': PlaceHolder('$', ['text'], pattern=r'\d{11}'),
        '人员ID': PlaceHolder('$', ['text'], pattern=r'\d{8}'),
        '人员姓名': PlaceHolder('$', ['text'], func=generate_name),
        '医疗机构代码': PlaceHolder('$', ['text'], pattern=r'\d{7}'),
        '疾病编码': PlaceHolder('$', ['text'], pattern=r'[A-Z]\d{2}\.(\d|X)\d{2}'),
        '疾病名称': PlaceHolder('$', ['text'], values=['2型糖尿病', '人格障碍', '低钾血症', '儿童孤独症', '关节炎',
            '冠状动脉粥样硬化性心脏病', '前列腺增生', '化脓性牙龈炎', '单纯型精神分裂症', '口齿病(龋齿病)', '后循环缺血', '嗜眠症',
            '器质性心境[情感]障碍', '器质性精神病', '器质性精神综合征', '复发性抑郁障碍', '复发性阿弗他溃疡', '多动性障碍', '失眠',
            '妄想型精神分裂症', '妊娠合并精神障碍', '尘肺', '帕金森病性痴呆(震颤麻痹性痴呆)', '带状疱疹', '广泛性焦虑障碍', '强迫性障碍',
            '心境[情感]障碍', '心脏病', '急性上呼吸道感染', '急性扁桃体炎', '急性支气管炎', '急性根尖周炎', '急性牙髓炎',
            '急性精神分裂症样精神病性障碍', '急性胃肠炎', '慢性咽炎', '慢性喉咽炎', '慢性支气管炎', '慢性根尖周炎', '慢性牙周炎',
            '慢性牙髓炎', '慢性紧张型头痛', '慢性胃溃疡', '慢性胃炎', '慢性阻塞性肺病伴有急性加重', '慢性鼻炎', '慢性龈炎', '抑郁症',
            '抽动秽语综合征', '抽动障碍', '持久的妄想性障碍', '持续的躯体形式的疼痛障碍', '支气管炎', '未分化型精神分裂症', '残根', '沙眼',
            '活动与注意失调[注意缺陷与多动障碍]', '混合型分裂情感性障碍', '混合型阿尔茨海默病性痴呆', '混合性焦虑和抑郁障碍',
            '混合性焦虑障碍', '湿疹', '焦虑障碍', '煤尘肺(炭末肺)', '煤工尘肺', '牙体缺损', '牙列缺失', '牙列缺损', '牙周脓肿', '牙折断',
            '牙本质过敏症', '牙本质龋', '牙隐裂', '牙齿楔状缺损', '牙龈出血', '特发性肌张力障碍', '特指甲状腺功能减退症',
            '由于使用其他兴奋剂引起的精神和行为障碍(包括咖啡因)', '由于使用酒精引起的精神和行为障碍', '由于使用酒精引起的精神病性障碍',
            '由于使用阿片类药引起的精神病性障碍', '病理性赌博', '痴呆', '瘙痒症', '癫痫', '癫痫性精神病', '白内障', '白细胞异常', '皮炎',
            '皮肤疖', '睡眠障碍', '矽肺(硅肺)', '矽肺(硅肺)Ⅲ期', '矽肺(硅肺)Ｉ期', '矽肺叁期', '矽肺壹期', '矽肺贰期', '社交恐怖',
            '神经衰弱', '童年情绪障碍', '童年离别焦虑障碍', '类风湿性关节炎', '精神分裂症', '精神分裂症后抑郁', '精神发育迟滞',
            '精神抑郁症', '精神病(门特)', '精神障碍', '糖尿病', '紫癜', '结膜炎', '继发龋', '维生素B缺乏病', '肝功能异常', '肾结石',
            '胃炎', '胆囊炎', '脑外伤所致精神障碍', '脑性瘫痪(脑瘫)', '脑梗死', '脑梗死后遗症', '脑膜瘤', '脑血管病所致的人格和行为障碍',
            '腔隙性脑梗死', '血管性痴呆', '谵妄', '躁狂型分裂情感性障碍', '躁狂型精神病', '躁狂抑郁性精神病',
            '躁狂抑郁性精神病当前为抑郁相', '躁狂抑郁性精神病当前为躁狂相', '躯体化障碍', '躯体形式障碍', '轻度精神发育迟滞',
            '轻度认知障碍', '过敏性皮炎', '酒精依赖综合征', '酒精性肝硬化', '阻生牙', '阿尔茨海默病', '阿尔茨海默病性痴呆',
            '非器质性失眠症', '非器质性睡眠障碍', '颅脑外伤所致的精神障碍', '高血压', '高血压性心脏病', '高血压病', '龈乳头炎']),
        '科室编码': PlaceHolder('$', ['text'], pattern=r'\d{3,5}'),
        '科室名称': PlaceHolder('$', ['text'], values=[
            ['综合内科', '内科', '普内'],
            ['心血管内科', '心内', '心血管内', '心内科'],
            ['呼吸内科', '呼吸内', '呼吸科'],
            ['神经内科', '神内科', '神内', '神经科', '神经内', '脑科', '脑病'],
            ['肾内科', '肾内', '肾科', '肾病'],
            ['消化内科', '消化内', '消化科'],
            ['血液科', '血液内科', '血液病'],
            ['内分泌科', '内分泌'],
            ['风湿免疫科', '免疫科', '风湿免疫', '风湿病'],
            ['老年病科', '老年科', '老年医学', '老年病', '老年保健'],
            ['感染科', '感染性疾病', '感染病'],
            ['传染病科', '传染科'],
            ['肝病科', '肝病'],
            ['综合外科', '大外科'],
            ['甲状腺外科', '甲状腺外', '甲状腺科', '甲状腺'],
            ['乳腺外科', '乳腺外', '乳腺科', '乳腺疾病', '乳腺'],
            ['普外科', '普外', '外科'],
            ['血管外科', '血管外'],
            ['胃肠外科', '胃肠外', '肠胃外科', '肠胃外', '肠胃科', '胃肠科'],
            ['肝胆胰外科', '肝胆胰', '肝胆胰外', '肝胆科', '肝胆胰科', '肝胆外科', '肝胆外'],
            ['肛肠外科', '肛肠外', '肛肠'],
            ['整形外科', '整形外', '整形科', '美容科', '美容外科', '整形', '美容', '整容'],
            ['泌尿外科', '泌尿', '泌尿外', '泌尿科'],
            ['烧伤科', '烧伤'],
            ['胸外科', '胸外'],
            ['心血管外科', '心外', '心血管外', '心外科'],
            ['神经外科', '神外', '神经外', '神外科', '脑外', '脑外科'],
            ['男科', '男性科'],
            ['妇产科'],
            ['计划生育科', '计划生育', '计生'],
            ['妇科'],
            ['妇科肿瘤科', '妇科肿瘤外科', '妇科肿瘤'],
            ['妇科内分泌科'],
            ['妇女保健科', '妇女保健', '妇保科'],
            ['产科'],
            ['产前诊断科', '产前诊断', '产前'],
            ['产后康复科', '产后康复'],
            ['母乳喂养咨询', '母乳喂养'],
            ['生殖医学科', '生殖科', '生殖医学', '生殖中心'],
            ['不孕不育科', '不孕科', '不育科', '不孕不育', '不育不孕', '不孕', '不育'],
            ['生殖内分泌'],
            ['试管婴儿中心'],
            ['医学遗传', '遗传科', '遗传', '医学遗传科'],
            ['优生咨询专科', '优生'],
            ['生殖男科'],
            ['儿科', '小儿科'],
            ['小儿外科'],
            ['新生儿科', '新生儿'],
            ['新生儿外科'],
            ['儿童保健科', '小儿保健科', '儿科保健科', '小儿保健', '儿保科', '儿童保健', '儿保'],
            ['小儿康复科', '儿科康复科', '小儿康复', '康复儿科'],
            ['小儿急诊科'],
            ['小儿呼吸内科', '小儿呼吸内', '小儿呼吸科', '小儿呼吸', '儿科呼吸内科', '儿科呼吸内', '儿科呼吸'],
            ['小儿心理科'],
            ['小儿精神科', '儿科精神科'],
            ['小儿营养科', '儿童营养科'],
            ['小儿骨科', '小儿骨外科'],
            ['小儿脊柱外科'],
            ['小儿足踝外科'],
            ['小儿关节外科', '小儿关节外', '小儿关节科', '小儿骨关节科', '小儿骨关节', '小儿关节炎', '小儿关节病'],
            ['小儿创伤骨科'],
            ['小儿矫形骨科'],
            ['小儿骨质疏松科'],
            ['小儿手外科'],
            ['小儿骨与软组织肿瘤科'],
            ['小儿运动医学科'],
            ['小儿皮肤科', '小儿皮肤'],
            ['小儿烧伤科'],
            ['小儿皮肤外科'],
            ['小儿整形外科'],
            ['小儿过敏反应科'],
            ['小儿性病科'],
            ['小儿普外科', '小儿普外', '儿科普外', '儿科普外科', '儿外科', '儿外'],
            ['小儿胃肠外科'],
            ['小儿肝胆胰外科'],
            ['小儿乳腺外科'],
            ['小儿甲状腺外科'],
            ['小儿神经外科'],
            ['小儿泌尿科', '小儿泌尿', '小儿泌尿外', '儿科泌尿外科', '儿科泌尿', '儿科泌尿外', '儿科泌尿科', '儿童泌尿科'],
            ['小儿耳鼻喉科'],
            ['小儿肛肠外科'],
            ['小儿头颈外科', '小儿头颈'],
            ['小儿风湿免疫科'],
            ['小儿内科', '儿内', '儿科内科', '小儿内'],
            ['小儿神经内科', '小儿神内', '小儿神经内', '儿科神经内科', '儿科神内儿科神经内', '小儿神经', '儿童神经'],
            ['小儿心血管内科', '小儿心血管', '儿科心血管内科', '儿科心内', '小儿心内', '儿科心内'],
            ['小儿内分泌科', '小儿内分泌', '儿科内分泌科', '儿科内分泌'],
            ['小儿血液科', '小儿血液', '儿科血液科', '儿科血液', '血液儿科', '小儿血液内科'],
            ['小儿肾内科', '小儿肾内', '儿科肾内科', '儿科肾内', '小儿肾科', '儿科肾科'],
            ['小儿消化科', '小儿消化', '小儿消化内', '儿科消化内科', '儿科消化内', '儿科消化', '小儿消化内科'],
            ['小儿眼科'],
            ['小儿角膜病科'],
            ['小儿屈光科'],
            ['小儿眼底病科'],
            ['小儿眼外伤科'],
            ['小儿白内障科'],
            ['小儿青光眼科'],
            ['小儿近视手术科'],
            ['小儿眼眶病与眼肿瘤科'],
            ['小儿眼整形科'],
            ['儿童口腔科', '小儿口腔科', '儿童口腔'],
            ['小儿口腔正畸科'],
            ['小儿口腔颌面外科'],
            ['小儿口腔黏膜科', '儿童口腔黏膜科', '小儿口腔黏膜'],
            ['小儿口腔种植科'],
            ['小儿牙体牙髓科'],
            ['小儿牙周病科'],
            ['小儿口腔修复科'],
            ['小儿口腔预防科'],
            ['小儿胸外科'],
            ['小儿心血管外科'],
            ['小儿传染病科', '小儿传染病', '小儿传染科'],
            ['小儿感染科', '小儿感染内科'],
            ['小儿男科'],
            ['小儿妇科'],
            ['小儿妇科肿瘤科'],
            ['小儿妇科内分泌'],
            ['小儿肿瘤科'],
            ['小儿肿瘤外科'],
            ['小儿化疗科', '小儿肿瘤内科'],
            ['小儿肿瘤介入科'],
            ['小儿PICC门诊'],
            ['小儿头颈肿瘤科'],
            ['小儿脑部肿瘤科'],
            ['小儿放射治疗科'],
            ['小儿腹部肿瘤科'],
            ['小儿泌尿肿瘤科'],
            ['小儿胸部肿瘤科'],
            ['小儿乳腺肿瘤科'],
            ['小儿肝脏肿瘤科'],
            ['小儿胃肠肿瘤科'],
            ['小儿麻醉科'],
            ['小儿疼痛科'],
            ['骨科', '骨外科'],
            ['手外科', '手外'],
            ['脊柱外科', '脊柱科', '脊柱外'],
            ['创伤骨科', '骨伤科', '骨伤'],
            ['关节外科', '关节外', '关节科', '骨关节科', '骨关节', '关节炎', '关节病'],
            ['骨质疏松科'],
            ['矫形骨科'],
            ['足踝外科', '足踝外'],
            ['运动医学科', '运动医学', '运动科'],
            ['显微创伤外科'],
            ['五官科'],
            ['耳鼻喉科', '耳鼻喉', '耳科', '鼻科', '喉科', '咽喉科', '耳鼻咽喉'],
            ['头颈外科', '头颈外'],
            ['眼科'],
            ['眼底病科', '眼底病'],
            ['角膜病科', '角膜病'],
            ['眼外伤科', '眼外伤'],
            ['屈光科', '视光学', '视光中心'],
            ['白内障科', '白内障'],
            ['准分子激光科', '准分子激光'],
            ['青光眼科', '青光眼'],
            ['近视手术科', '近视手术'],
            ['眼眶病与眼肿瘤科'],
            ['眼整形科', '眼部整形', '眼睛整形', '眼整形'],
            ['口腔综合科', '牙科', '牙病科', '口腔内科', '口腔科'],
            ['牙周病科', '牙周科', '牙周'],
            ['口腔黏膜科', '口腔黏膜'],
            ['口腔种植科', '种植科', '种植'],
            ['口腔正畸科', '口腔正畸', '正畸', '牙齿矫正'],
            ['牙体牙髓科', '牙体牙髓', '补牙'],
            ['口腔颌面外科', '颌面外科', '拔牙', '口腔外科'],
            ['口腔修复科', '口腔修复'],
            ['口腔预防科', '口腔预防'],
            ['皮肤科', '皮肤'],
            ['性病科', '性病'],
            ['过敏反应科', '变态反应科', '过敏反应', '变态反应'],
            ['皮肤外科', '皮肤外'],
            ['肿瘤科', '肿瘤专科', '肿瘤门诊', '肿瘤'],
            ['放射治疗科', '放疗科', '放疗'],
            ['化疗科', '肿瘤内科'],
            ['肿瘤介入科', '肿瘤介入'],
            ['PICC门诊', 'PICC', '静脉导管'],
            ['脑部肿瘤科', '脑部肿瘤外科', '脑部肿瘤'],
            ['头颈肿瘤科', '头颈肿瘤外科', '头颈肿瘤'],
            ['口腔肿瘤科', '口腔肿瘤', '口腔颌面肿瘤'],
            ['胸部肿瘤科', '胸部肿瘤外科', '胸部肿瘤'],
            ['腹部肿瘤科', '腹部肿瘤外科', '腹部肿瘤'],
            ['乳腺肿瘤科', '乳腺肿瘤外科', '乳腺肿瘤', '乳腺癌'],
            ['肝脏肿瘤科', '肝脏肿瘤外科', '肝脏肿瘤'],
            ['胃肠肿瘤科', '胃肠肿瘤外科', '胃肠肿瘤'],
            ['泌尿肿瘤科', '泌尿肿瘤外科', '泌尿肿瘤'],
            ['骨与软组织肿瘤科', '骨肿瘤科', '软组织肿瘤科', '骨肿瘤', '软组织肿瘤'],
            ['肿瘤外科'],
            ['中医科', '中医'],
            ['治未病科'],
            ['中医正骨科', '正骨'],
            ['中医针灸科', '针灸'],
            ['中医心血管病专科', '中医心血管病科'],
            ['中医推拿科', '推拿'],
            ['中医伤科'],
            ['中医内分泌科', '中医内分泌'],
            ['中医肝病科', '中医肝病'],
            ['中医风湿免疫病科', '中医风湿科', '中医免疫科'],
            ['中医儿科', '小儿中医科'],
            ['中医康复科', '中医康复'],
            ['中医妇科'],
            ['中医外科', '中医普外'],
            ['中医肾病内科', '中医肾病科', '中医肾病'],
            ['中西医结合科学', '中西医结合科', '中西医结合'],
            ['麻醉科', '麻醉'],
            ['疼痛科', '疼痛专科'],
            ['体检科', '体检'],
            ['预防保健科'],
            ['核酸检测', '新冠核酸', '核酸', '核酸检查', '新冠检测', '复工复产', '复工', '复产'],
            ['精神科', '精神'],
            ['心理科', '心理'],
            ['全科医学科', '全科', '全医学科'],
            ['慢病科'],
            ['重症医学科', '重症医学', 'ICU'],
            ['急诊科', '急诊'],
            ['介入医学科', '介入科', '介入治疗'],
            ['康复科', '康复理疗', '康复医学'],
            ['营养科', '营养咨询'],
            ['高压氧科', '高压氧'],
            ['职业病科'],
            ['护理科'],
            ['伤口造口门诊', '伤口造口', '换药'],
            ['检验科'],
            ['影像科'],
            ['超声科', '超声室', '超声'],
            ['内镜中心', '内镜科', '内镜', '胃镜', '肠镜', '腔镜', '管镜'],
            ['心电图室'],
            ['行政科'],
            ['药房'],
            ['放射科'],
            ['核医学科', '核医学'],
            ['病理科'],
            ['药剂科'],
            ['其他学科', '其他', '其它', '其他科室']
        ]),
        '人员医疗费用明细ID': PlaceHolder('$', ['text'], pattern=r'\d{11}'),
        '社保三大目录统一编码': PlaceHolder('$', ['text'], pattern=r'(\d{4}|\d{6}|\d{9})(-(\d|[a-z]))?'),
        '社保三大目录名称': PlaceHolder('$', ['text'], values=['丁酸氢化可的松乳膏', '三九胃泰颗粒', '三拗片(薄膜衣)',
            '丙戊酸钠片(糖衣)', '丙戊酸钠缓释片', '丙戊酸镁缓释片', '丙酸氟替卡松鼻喷雾剂', '乌灵胶囊', '九味镇心颗粒', '乳果糖口服溶液',
            '云南白药胶囊', '五氟利多片(糖衣)', '佐匹克隆片(薄膜衣)', '佛手颗粒', '克拉霉素分散片', '六味地黄丸', '兰索拉唑肠溶片',
            '养心氏片(薄膜衣)', '利可君片(薄膜衣)', '利培酮分散片', '利培酮口服液', '利培酮口服溶液', '利培酮口腔崩解片',
            '利培酮片(薄膜衣)', '劳拉西泮片', '北沙参颗粒', '单硝酸异山梨酯片', '卡马西平片', '厄贝沙坦片(薄膜衣)', '厚朴花颗粒',
            '双氯芬酸二乙胺乳胶剂', '右佐匹克隆片', '叶酸片', '合欢皮颗粒', '吡拉西坦片', '吡诺克辛滴眼液', '吲哚美辛栓',
            '吸入用乙酰半胱氨酸溶', '吸入用复方异丙托溴铵', '吸入用布地奈德混悬液', '呋塞米片', '哈西奈德溶液', '噻托溴铵粉吸入剂',
            '地氯雷他定干混悬剂', '地衣芽孢杆菌活菌胶囊', '地西泮片', '培哚普利叔丁胺片', '复合维生素B片', '复方丙酸氯倍他索软膏',
            '复方丹参滴丸', '复方氨酚烷胺胶囊', '复方氯己定含漱液', '复方甲氧那明胶囊', '复方盐酸伪麻黄碱缓释胶囊', '复方聚乙二醇电解质散',
            '复方鲜竹沥液', '多巴丝肼片', '多潘立酮片', '多糖铁复合物胶囊', '天冬酸氨基转移酶线粒', '头孢丙烯片(薄膜衣)', '头孢克肟分散片',
            '奋乃静片(薄膜衣)', '奥卡西平片(薄膜衣)', '奥氮平片', '奥氮平片(薄膜衣)', '奥沙西泮片', '奥硝唑胶囊', '奥美拉唑镁肠溶片',
            '妥布霉素滴眼液', '富马酸喹硫平片(薄膜)', '尿素乳膏', '川石斛颗粒', '左氧氟沙星滴眼液', '左甲状腺素钠片', '布洛芬片(糖衣)',
            '布洛芬缓释胶囊', '帕利哌酮缓释片', '开塞露(含甘油)', '强力枇杷露(无糖型)', '急支糖浆', '恩替卡韦分散片', '扎来普隆分散片',
            '托吡酯片(薄膜衣)', '抗病毒口服液', '抗病毒颗粒', '护肝宁片(薄膜衣)', '拉莫三嗪片', '替米沙坦片', '木丹颗粒',
            '枸地氯雷他定片(薄膜)', '枸橼酸坦度螺酮胶囊', '柏子仁颗粒', '格列美脲片', '格列齐特缓释片', '桂林西瓜霜', '桔梗颗粒',
            '止嗽化痰颗粒', '氟哌啶醇片(糖衣)', '氟哌噻吨美利曲辛片', '氢氯噻嗪片', '氨磺必利片', '氯化钾缓释片', '氯氮平片', '氯硝西泮片',
            '氯雷他定片', '汉防己甲素片(薄膜衣)', '消旋山莨菪碱片', '消炎利胆片(糖衣)', '清热散结胶囊', '清脑复神液', '炙远志颗粒',
            '玻璃酸钠滴眼液', '珍珠明目滴眼液', '琥珀酸美托洛尔缓释片', '瑞舒伐他汀钙片', '甘草颗粒', '甜梦口服液', '生地黄颗粒',
            '甲钴胺胶囊', '百乐眠胶囊', '益心舒胶囊', '盐酸丁螺环酮片', '盐酸二甲双胍肠溶胶囊', '盐酸倍他司汀片(糖衣)', '盐酸哌甲酯缓释片',
            '盐酸多塞平片(糖衣)', '盐酸多奈哌齐片(薄膜)', '盐酸多奈哌齐胶囊', '盐酸小檗碱片(糖衣)', '盐酸左氧氟沙星胶囊', '盐酸帕罗西汀片',
            '盐酸帕罗西汀片(薄膜)', '盐酸度洛西汀肠溶片', '盐酸度洛西汀肠溶胶囊', '盐酸托莫西汀胶囊', '盐酸文拉法辛缓释片',
            '盐酸文拉法辛缓释胶囊', '盐酸文拉法辛胶囊', '盐酸普罗帕酮片', '盐酸氟桂利嗪胶囊', '盐酸氟西汀分散片', '盐酸氟西汀片',
            '盐酸氨基葡萄糖胶囊', '盐酸氯丙嗪片(糖衣)', '盐酸氯米帕明片(糖衣)', '盐酸硫必利片', '盐酸米安色林片(薄膜)', '盐酸米那普仑片',
            '盐酸美金刚口服溶液', '盐酸美金刚片(薄膜衣)', '盐酸胺碘酮片', '盐酸舍曲林片', '盐酸舍曲林片(薄膜衣)', '盐酸舍曲林胶囊',
            '盐酸苯海索片', '盐酸贝那普利片(薄膜)', '盐酸金霉素眼膏', '盐酸阿米替林片(薄膜)', '盐酸齐拉西酮胶囊', '硝苯地平控释片',
            '硝苯地平片(糖衣)', '硝苯地平缓释片(Ⅰ)', '硝西泮片', '硝酸咪康唑乳膏', '硫酸氢氯吡格雷片', '硫酸阿托品片',
            '碳酸钙D3片(薄膜衣)', '碳酸锂片', '碳酸锂缓释片', '稳心颗粒', '米氮平片(薄膜衣)', '红霉素软膏', '维A酸乳膏', '维生素B1片',
            '维生素B2片', '维生素B6片', '维生素C片', '缬沙坦胶囊', '罗红霉素胶囊', '胃苏颗粒(无糖型)', '胆宁片(薄膜衣)', '胞磷胆碱钠片',
            '胰激肽原酶肠溶片', '脑心通胶囊', '舒必利片', '舒肝解郁胶囊', '艾司唑仑片', '艾司奥美拉唑镁肠溶片', '芪胶升白胶囊',
            '苏黄止咳胶囊', '苯妥英钠片', '苯巴比妥片', '苯磺酸左旋氨氯地平片', '苯磺酸氨氯地平片', '草酸艾司西酞普兰片', '葡醛内酯片',
            '蒙脱石散', '蒲地蓝消炎口服液', '蓝芩口服液', '蜜炼川贝枇杷膏', '螺内酯片', '血塞通软胶囊', '补肺活血胶囊', '西帕依固龈液',
            '谷维素片', '连花清瘟胶囊', '速效救心丸', '酒石酸唑吡坦片', '酒石酸美托洛尔片', '酸枣仁颗粒', '醋酸地塞米松片', '醋酸泼尼松片',
            '重酒石酸卡巴拉汀胶囊', '金水宝片', '金荞麦片(薄膜衣)', '铝碳酸镁咀嚼片', '铝碳酸镁片', '银杏叶片(薄膜衣)', '阿卡波糖片',
            '阿司匹林肠溶片', '阿戈美拉汀片', '阿托伐他汀钙片(薄膜)', '阿普唑仑片', '阿立哌唑口腔崩解片', '阿立哌唑片', '阿莫西林胶囊',
            '雷贝拉唑钠肠溶片', '非洛地平缓释片', '非诺贝特胶囊', '非那雄胺片(薄膜衣)', '香砂养胃丸', '马应龙麝香痔疮膏',
            '马来酸依那普利片', '骨化三醇软胶囊', '麝香保心丸', '麝香追风膏', '麦冬颗粒', '黄氏响声丸(炭衣浓缩)']),
        '门诊就诊流水号': PlaceHolder('$', ['text'], pattern=r'\d{11}'),
        '住院就诊流水号': PlaceHolder('$', ['text'], pattern=r'\d{11}'),
        '门诊就诊流水号或住院就诊流水号': PlaceHolder('$', ['text'], pattern=r'\d{11}'),
        '医生工号': PlaceHolder('$', ['text'], pattern=r'\d{8}'),
        '检验报告单号': PlaceHolder('$', ['text'], pattern=r'\d{11}'),
        '检验指标流水号': PlaceHolder('$', ['text'], pattern=r'\d{11}'),
        '检测人工号': PlaceHolder('$', ['text'], pattern=r'\d{8}'),
        '检测人姓名': PlaceHolder('$', ['text'], func=generate_name),
        '检测指标代码': PlaceHolder('$', ['text'], pattern=r'\d{6}'),
        '检测指标名称': PlaceHolder('$', ['text'], values=['总胆红素三代', '直接胆红素二代', '总蛋白', '白蛋白', '脂肪酶', '前白蛋白',
            '尿素', '胱抑素C2代', '同型半胱氨酸', '果糖胺', '甘油三酯', '胆固醇', '低密度脂蛋白胆固醇', '脂蛋白(a)二代', '肌酸激酶同工酶',
            'α-羟丁酸脱氢酶', '二氧化碳', '类风湿因子', 'C反应蛋白', '补体C3', '补体C4', '免疫球蛋白A(标准)', '免疫球蛋白A(敏感)',
            '免疫球蛋白M(标准)', '免疫球蛋白M(敏感)', 'a1酸性糖蛋白', 'a1抗胰蛋白酶', '抗凝血酶III', 'D2聚体(柠檬酸盐)',
            'D2聚体(肝素/EDTA)', '触珠蛋白', 'B2微球蛋白', '血清铁', '转铁蛋白', '胸腹水白蛋白(白蛋白)', '苯巴比妥', '苯妥因', '茶碱',
            '丙戊酸', '甲胎蛋白', '糖类抗原125', '糖类抗原724', '游离前列腺特异性抗原', '胃泌素释放肽前体', '神经元特异性烯醇化酶',
            '细胞角蛋白19片段', '罗马指数(绝经前)', '罗马指数(绝经后)', 'S100', '三碘甲状腺原氨酸', '甲状腺素', '游离三碘甲状腺原氨酸',
            '游离甲状腺素', '游离甲状腺素(三代)', '促甲状腺激素', '甲状腺过氧化物酶抗体', '促甲状腺激素受体抗体', '超敏甲状腺球蛋白',
            '甲状腺摄取实验', '促肾上腺皮质激素', '妊娠相关性血浆蛋白-A', '游离β-绒毛膜促性腺激素', '氨基末端B型利钠肽', '超敏肌钙蛋白T',
            '地高辛', '洋地黄', '乙肝表面抗原(定量)', '甲状旁腺素', '全段甲状旁腺激素', '叶酸', '白介素-6', '降钙素原', '抗环瓜氨酸肽抗体']),
        '部位': PlaceHolder('$', ['text'], values=['头部', '颅部', '脸部', '颈部', '肩部', '胸部', '背部', '腰部', '上臂', '上肢',
            '肘部', '前臂', '腕部', '手部', '臀部', '大腿', '下肢', '小腿', '踝部', '足部'])
    }
    value_sets = {}
    for key in place_holders:
        value_sets[key] = set()
    data = pd.read_excel('templates.xlsx', skiprows=10)
    dataset = []
    for i in range(len(data)):
        if data['难度'][i] == '不可回答':
            continue
        question_template = data['查询模板'][i]
        sql_template = data['SQL模板'][i]
        for _ in range(10):
            all_values = []
            all_types = []
            question = ''
            end = -1
            while 1:
                start = question_template[end + 1:].find('（') + end + 1
                if start <= end:
                    question += question_template[end + 1:]
                    break
                question += question_template[end + 1:start]
                end = question_template[start:].find('）') + start
                place_holder = question_template[start + 1:end]
                string, values = place_holders[place_holder].generate()
                question += string
                all_values.extend(values)
                all_types.extend(place_holders[place_holder].types)
                value_sets[place_holder].update(values)
            sql = ''
            end = -1
            while 1:
                start = sql_template[end + 1:].find('$') + end + 1
                if start <= end:
                    sql += sql_template[end + 1:]
                    break
                sql += sql_template[end + 1:start]
                end = start + 1
                while end + 1 < len(sql_template) and sql_template[end + 1] >= '0' and sql_template[end + 1] <= '9':
                    end += 1
                idx = int(sql_template[start + 1:end + 1]) - 1
                if all_types[idx] == 'number':
                    sql += all_values[idx]
                elif all_types[idx] == 'text':
                    sql += f"'{all_values[idx]}'"
                else:
                    raise ValueError
            dataset.append({
                'template': i,
                'question': question,
                'sql': sql,
                'schema': data['数据库'][i],
                'level': data['难度'][i]
            })
    with open('dataset.json', 'w', encoding='utf-8') as file:
        json.dump(dataset, file, ensure_ascii=False, indent=4)
    for key in value_sets:
        value_sets[key] = list(value_sets[key])
    return value_sets
