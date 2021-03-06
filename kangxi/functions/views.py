# coding: utf8
from flask import render_template, request, Blueprint, jsonify
from kangxi import db
from .forms import characterSearchForm, synonymousCharactersForm, treeForm, treeSearchForm, meaningSearchForm
import sqlalchemy as sa
import urllib
from collections import Counter


functions = Blueprint('functions', __name__)


kangxi = db.Table('kangxi', db.metadata, autoload=True, autoload_with=db.engine)
meanings = db.Table('meanings', db.metadata, autoload=True, autoload_with=db.engine)
radicals = db.Table('radicals', db.metadata, autoload=True, autoload_with=db.engine)


@functions.route('/tools', methods=['GET', 'POST'])
def tools():
    
    charSearchForm = characterSearchForm()
    synCharForm = synonymousCharactersForm()
    trForm = treeForm()
    trSearchForm = treeSearchForm()
    meanSearchForm = meaningSearchForm()
    rads = db.session.query(radicals).all()
    
    return render_template('tools.html',
                            charSearchForm=charSearchForm,
                            synCharForm=synCharForm,
                            trForm=trForm,
                            trSearchForm=trSearchForm,
                            meanSearchForm=meanSearchForm,
                            rads=rads)


@functions.route('/home')
def home():

    return render_template('index.html')


@functions.route('/about')
def about():

    twoRadRoots = '''一丿𠂇	一乙七	一乙𠀁	一人亼	一入𠓛	一冂𠀃	一凵廿	一卜上	一宀㝉	一小朩	 
            一屮㞢	一廾井	一斤丘	一日旦	一木未	一木末	一木本	一氏氐	丨弓弔	丨彐丑	 
            丨无旡	丶乙龴	丶几凡	丶刀刃	丶勹勺	丶大太	丿一丆	丿丿㐅	丿丿乂	丿丿𠂆	 
            丿乙𠂊	丿小少	丿尸尺	丿戈戊	乙一丂	乙乙乜	乙乙𠄎	乙亠亡	乙人乞	乙人亾	 
            乙十㐄	乙大夬	乙工五	乙己㠯	乙穴穵	亅一丁	亅丨丩	亅丿𠂈	亅乙了	亅乙𠄐	 
            亅二于	亅二𠂌	亅戈戉	二一三	二丨𠀆	二人夫	二冂冃	二勹勻	二弋弍	二欠次	 
            亠冂丹	人一𠆣	人二仁	人人久	人人仌	人人从	人冂𠔿	人匕化	人寸付	人弋代	 
            人戈伐	人木休	人犬伏	人立位	人聿伊	人臼臾	人艸𦫸	人門閃	人隹倠	人靑倩	 
            人鳥𠌵	儿一兀	儿二元	儿厶允	儿口兄	儿土圥	儿牛先	儿白皃	儿羊羌	儿臼兒	 
            儿虍虎	儿音竟	入入𠓜	八亠六	八人介	八口只	八大𡗜	八干平	八羊𦍎	冂入內	 
            冂土冉	冂大央	冂木朿	冖小龸	冖艸𫇦	冫人仒	冫夂冬	冫弓𢎥	冫馬馮	几亠亢	 
            几冖冗	几禾秃	凵冂凸	凵凵凹	凵土凷	凵屮出	凵車𨊥	刀八分	刀口叧	力力𠠴	 
            力口加	力口另	力夂务	力田男	勹网𦉶	匕匕北	匕宀它	匕日㫐	匕白皀	匕矢𠤑	 
            匕頁頃	匚口叵	匚己巨	匚巾匝	匚玉匡	匚非匪	匸儿匹	匸矢医	十丨卄	十丿千	 
            十乙卂	十人仐	十人午	十匕𠤏	十大夲	十日早	十水𠦂	十田卑	十隹隼	十音章	 
            卜一下	卜卜卝	卩又𠬝	厂人仄	厂刀厃	厂卩厄	厂又反	厂山屵	厂里厘	厶丿么	 
            厶二云	厶亠𠫓	厶八公	厶厶厸	厶土去	又丶叉	又刀𠬛	又又双	又屮𠬢	又爪𠬪	 
            又隹隻	口一𠮛	口八㕣	口冂冋	口刀召	口刀𠮥	口勹句	口十古	口卜占	口卩叩	 
            口厶台	口又叹	口口吅	口口吕	口土𠮷	口士吉	口夂各	口夕名	口寸吋	口戈戓	 
            口文吝	口木杏	口木束	口牛吿	口立咅	口聿君	口衣哀	口車軎	口隹唯	囗丨中	 
            囗人囚	囗儿四	囗口回	囗大因	囗己囙	囗木困	囗禾囷	囗豕圂	囗韋圍	土丿𡈼	 
            土八𡉀	土又圣	土土圭	土方坊	土欠坎	土殳坄	土比坒	土穴𥤧	土艸芏	土西垔	 
            土革堇	土黑墨	士一壬	夂几処	夂卜处	夊心𢖻	夊鹿𪊎	夕卩夗	夕夕多	夕巛𡿪	 
            大一天	大丿夭	大日旲	大羊美	大而耎	大西䙲	女又奴	女口如	女女奻	女子好	 
            女宀安	女日妟	女爪妥	女禾委	女立妾	女西要	子乙孔	子子孖	子宀字	子日㫗	 
            子爪孚	子瓜孤	子禾季	子老孝	寸士寺	寸宀守	寸彐寻	寸爪寽	寸辰辱	小人尒	 
            小刀尔	小日𣌢	尢丶尤	尢力𡯄	尸丨𠃜	尸二𡰥	尸匕尼	尸口𡰪	尸尸𡰲	尸巾𡰯	 
            尸支𡰸	尸毛尾	尸水尿	尸至屋	尸辛屖	尸雨屚	屮艸屰	山人仚	山攴𡵲	山网岡	 
            山鳥島	工人仝	工弋式	工穴空	工羊差	工頁項	己丨巴	己勹包	巾一帀	巾亠市	 
            巾几凧	巾口吊	巾白帛	巾艸芇	干八𢆉	干干幵	干日旱	幺力幼	幺幺𢆶	幺邑𨙵	 
            广隶康	广鬼廆	广黃廣	廴聿建	廾一开	廾丿升	廾十卉	廾厶弁	廾戈戒	廾玉弄	 
            廾臼舁	弓丨引	弓厶弘	弓大夷	弓弓弜	弓耳弭	弓隹雋	彐一互	彐刀刍	彐疋疌	 
            彐雨雪	彡人㐱	彡頁須	彳殳役	彳聿律	心丿必	心人𠇍	心士志	心己忌	心弋忒	 
            心心𢗰	心田思	心自息	心舌恬	心門悶	心隹惟	心音意	心頁㥑	戈十𢦏	戈戈戔	 
            戶乙戹	戶口启	戶攴𢼄	戶斤所	戶犬戾	戶羽扇	戶肉肩	戶邑扈	戶隹雇	手口扣	 
            手戈我	手手𢪒	手支技	手斤折	手爪抓	手甘拑	手白拍	手立拉	手臼㧮	手隹推	 
            攴目𥄎	文虍虔	斤丶斥	斤斤斦	斤欠欣	方人㫃	方攴放	日乙电	日勹旬	日匕旨	 
            日月明	日木東	日氏昏	日水沓	日老者	日老耆	日魚魯	曰日昌	曰聿書	月刀刖	 
            月月朋	月門閒	木丶朮	木乙札	木口呆	木斤析	木日杲	木木林	木木𣏟	木爪采	 
            木甘某	木田果	木白𣐩	木目相	木矛柔	木石䂞	木立亲	木网罙	木自臬	木舛桀	 
            木西栗	木酉梄	木高槀	木黃橫	止一正	止匕此	止止步	止止歨	止頁頉	歹刀列	 
            歹匕死	歹又𣦼	歹韭𩐁	殳癶癹	毋丶母	比日昆	毛毛㲎	氏口民	氏田畏	水丶永	 
            水乙氶	水人氽	水卩氾	水工汞	水工江	水彐彔	水彐录	水斤沂	水木沐	水欠㳄	 
            水水沝	水白泉	水白泊	水皮波	水网眔	水舌活	水隹淮	水高滈	火口𤆗	火大𤆍	 
            火彐灵	火火炎	火火炏	火羊羔	火聿㶳	火隹焦	火頁煩	火鹿麃	父亠交	爻爻㸚	 
            爿士壯	爿宀𪧇	爿戈戕	牛厶牟	牛宀牢	犬火狄	犬犬㹜	犬玉狂	犬目狊	犬穴突	 
            犬自臭	犬言狺	玉丶主	玉入全	玉口呈	玉玉玨	玉白珀	玉白皇	玉缶珤	瓜瓜㼌	 
            瓜穴窊	瓦冖𤬦	甘欠𣢟	生一𤯔	生日星	田亠亩	田十𤰔	田夂备	田大奋	田巛甾	 
            田玄畜	田田畕	田艸苗	田虍𧆨	田釆番	田雨雷	疋宀定	疋日是	疒矢疾	白一百	 
            白比皆	白白㿟	白羽習	皿子孟	皿日昷	皿水泴	目十𥃭	目日冒	目目䀠	目竹𥬥	 
            目米眯	矛攴敄	矢匕𠤕	矢厶矣	矢口知	矢隹雉	石山岩	石石砳	石麻磨	示大奈	 
            示宀宗	示木柰	示示祘	示西票	禸田禺	禾刀利	禾火秋	禾禾秝	立日昱	立立竝	 
            米入籴	米勹匊	米气氣	米臼䊆	米西粟	米頁頪	糸丿系	糸乙糺	糸寸紂	糸工紅	 
            糸田累	糸糸絲	糸色絕	糸隹維	缶勹匋	缶卩卸	网艸𦭝	羊土𦍒	羽日𦐇	而山耑	 
            而雨需	耳乙耴	耳又取	耳口咠	耳火耿	耳耳聑	耳邑耶	聿刀争	聿爪爭	聿竹筆	 
            聿艸芛	肉八䏌	肉八𦘩	肉力肋	肉厶䏍	肉口肙	肉小肖	肉幺𦘷	肉止肯	肉犬肰	 
            肉田胃	肉疋胥	肉豕豚	肉辰脣	臣人臥	臣又臤	臣己巸	自一𦣻	至刀到	至攴致	 
            至穴窒	臼丨𦥔	臼刀臽	臼干臿	臼爪舀	舌人舍	舛米粦	舟二亙	舟殳般	艮丶良	 
            虫丿䖝	虫口虽	虫虫䖵	行水衍	行韋衞	衣士表	見艸莧	角斗斛	角牛𧣈	言刀䚯	 
            言勹訇	谷卩卻	谷宀容	谷欠欲	豆十壴	豆山豈	豆癶登	豆虍䖒	豕丶豖	豕八㒸	 
            豕宀家	豕彐彖	豕生甤	豕立豙	豕虍豦	豕豕豩	豕高豪	豸艮貇	豸里貍	貝刀則	 
            貝刀負	貝卜貞	貝口員	貝小𧴪	貝攴敗	貝毋貫	貝网買	貝西賈	貝貝賏	赤攴赦	 
            赤赤赫	身寸射	身弓躬	車乙軋	車冖軍	車卩𨊠	車斤斬	車車䡛	辛宀宰	辛辛辡	 
            辵米迷	辵肉迌	辵艮退	辵豕逐	辵車連	辵隹進	辵首道	邑巛邕	酉八酋	釆宀宷	 
            釆穴𥦓	里立童	金欠欽	門文閔	門玉閏	阜力阞	阜肉阴	隹大奞	隹宀隺	隹山崔	 
            隹羽翟	隹艸萑	隹艸雈	隹虍雐	隹隹雔	隹雨霍	非网罪	非麻靡	革力勒	革月䩗	 
            革馬䩻	韭齊齏	音戈戠	音欠歆	風風䬕	食人飤	食羊養	馬衣褭	高欠歊	高艸蒿	 
            鬲虍鬳	鬲鳥鷊	魚禾穌	魚羊鮮	魚艸䔡	魚魚䲆	鳥一烏	鳥一𩾏	鳥鹿廌	鼠巛巤	 
            鼠穴竄	龠頁龥'''

    twoRadTrees = '''𠂇	在	茬	存	栫	荐	丈	仗	杖	粀	九	㐤	丸	紈	骫	㐇	仇	虓	卆	伜	厹	㐡	宄	尻	旭	旮	朹	氿	染	究	艽	訄	軌	匭	頄	馗	鳩	鼽	冇	厷	𠫤	恡	吰	宏	鋐	竑	紘	肱	谹	鈜	閎	雄	友	叐	爰	媛	援	暖	湲	緩	褑	諼	鍰	犮	冹	帗	拔	沷	祓	紱	胈	茇	蛂	跋	軷	鈸	韍	髪	魃	鮁	右	佑	𥁓	醢	祐	若	偌	匿	慝	暱	喏	婼	惹	掿	箬	諾	鍩	左	𢀡	隓	佐	惰	鬌	布	希	俙	唏	悕	晞	欷	烯	瓻	睎	稀	絺	莃	豨	鵗	佈	怖	戎	娀	毧	狨	絨	羢	茙	賊	駥	有	肴	殽	淆	侑	囿	宥	痏	賄	郁	灰	恢	盔	脄	詼	 
七	乇	仛	吒	奼	宅	侘	咤	姹	詫	托	秅	託	屯	囤	坉	忳	扽	杶	沌	㹠	盹	砘	純	肫	芚	鈍	頓	噸	魨	切	沏	砌	㲺	柒	 
𠀁	亐	 
亼	今	吟	含	唅	㟏	焓	琀	谽	頷	岑	梣	涔	念	唸	埝	捻	敜	棯	淰	稔	腍	諗	錜	鯰	琴	矜	紟	芩	衾	搇	衿	貪	嗿	酓	盦	韽	鈐	靲	黔	合	佮	㓣	箚	匼	哈	姶	峇	帢	弇	揜	渰	鞥	恰	拾	拿	嗱	敆	㭘	洽	盒	祫	答	劄	給	翕	噏	歙	闟	耠	荅	剳	嗒	塔	搭	溚	瘩	褡	蛤	袷	跲	鉿	閤	韐	頜	餄	鴿	龕	會	儈	劊	噲	廥	𢶒	檜	澮	燴	獪	禬	繪	膾	薈	襘	鬠	鱠	 
𠓛	兪	偸	喩	婾	愈	癒	愉	揄	楡	歈	渝	蕍	牏	瑜	瘉	窬	緰	羭	萮	蝓	褕	覦	諭	踰	輸	逾	鍮	隃	 
𠀃	具	俱	俱	埧	椇	犋	颶	直	值	真	傎	嗔	寘	慎	搷	滇	瑱	瘨	瞋	磌	禛	稹	縝	衠	𧽍	鎮	闐	顛	癲	鬒	齻	埴	植	殖	淔	犆	矗	稙	置	且	伹	冝	疊	㲲	助	勗	耡	莇	鋤	咀	姐	宜	誼	岨	徂	柤	査	揸	楂	渣	殂	沮	菹	狙	疽	砠	祖	租	蒩	粗	組	𦊕	苴	虘	摣	樝	皻	蔖	齇	蛆	詛	趄	鉏	阻	雎	駔	齟	麆	 
廿	丗	棄	世	屉	屜	屧	抴	枻	枼	偞	喋	堞	媟	惵	揲	渫	牒	碟	緤	艓	葉	蝶	諜	蹀	韘	鰈	泄	紲	貰	勩	迣	靾	齛	帶	墆	殢	滯	蔕	遰	卋	枽	度	剫	渡	踱	鍍	席	蓆	褯	庶	嗻	摭	蔗	䗪	蹠	遮	𣏼	 
上	卡	佧	咔	拤	胩	尗	戚	墄	慼	摵	槭	蹙	鏚	顣	叔	俶	寂	惄	椒	淑	琡	督	菽	裻	踧	敊	鮛	 
㝉	伫	𡧆	寅	夤	戭	演	瞚	縯	蔩	螾	賓	儐	嬪	擯	檳	殯	濱	矉	繽	薲	蠙	鑌	髕	鬢	 
朩	余	叙	徐	悆	敘	漵	斜	涂	塗	蒤	畬	稌	筡	荼	賒	䟻	途	酴	除	雓	餘	駼	鵌	杀	刹	弑	殺	殺	摋	榝	𥻦	鎩	 
㞢	蚩	嗤	媸	媸	 
井	𠀎	𡨄	寒	寋	塞	僿	㩙	簺	搴	寨	㩟	褰	謇	賽	㘔	蹇	瀽	騫	鶱	襄	嚷	囊	攮	灢	饢	齉	壤	孃	懹	攘	曩	瀼	瓖	瓤	禳	穰	䉴	纕	蠰	𧟄	讓	釀	鑲	驤	刱	耕	阱	 
丘	兵	浜	虡	岳	蚯	邱	 
旦	亘	咺	垣	宣	喧	揎	暄	楦	渲	煊	萱	諠	峘	晅	桓	烜	狟	荁	但	亱	曁	亶	壇	嬗	擅	檀	澶	𤺺	䄠	䉡	繵	羶	饘	鱣	坦	㝵	得	怛	担	喳	猹	碴	蹅	疸	笪	晝	袒	量	糧	鉭	靼	 
未	朱	侏	制	掣	猘	製	咮	姝	株	殊	珠	硃	蛛	袾	誅	跦	銖	𠩺	剺	嫠	氂	漦	釐	味	菋	妹	昧	沬	眛	魅	 
末	帓	抹	沫	秣	茉	袜	靺	韎	䱅	 
本	体	呠	笨	苯	鉢	 
氐	低	厎	坻	底	弤	抵	柢	眡	砥	祗	羝	蚳	袛	觝	詆	軧	邸	骶	鴟	 
弔	弟	俤	剃	娣	悌	晜	梯	涕	睇	稊	第	綈	䏲	銻	鵜	 
丑	吜	妞	忸	扭	杻	狃	峱	莥	紐	羞	饈	衄	鈕	 
旡	㤅	 
龴	令	伶	冷	囹	怜	拎	泠	狑	玲	瓴	笭	翎	聆	舲	苓	詅	軨	鈴	零	領	嶺	齡	𤔔	亂	薍	辭	甬	俑	勇	捅	桶	涌	痛	筩	蛹	誦	踊	通	𢳟	熥	 
凡	巩	恐	筑	築	蛩	跫	銎	鞏	帆	梵	汎	䏎	芃	軓	釩	 
刃	丒	歰	澀	刅	梁	粱	仞	忍	認	牣	紉	訒	軔	韌	 
勺	尥	彴	杓	汋	灼	瓝	的	啲	菂	約	喲	箹	葯	豹	趵	酌	釣	靮	馰	 
太	呔	忲	汰	肽	酞	鈦	 
丆	丌	亓	畀	淠	痹	箅	万	厉	不	丕	伾	呸	坯	歪	狉	秠	胚	駓	魾	吥	否	桮	痞	 	抔	杯	紑	罘	衃	鈈	阫	 
㐅	囪	凶	㐫	离	禽	噙	擒	𠌯	摛	樆	縭	螭	醨	離	灕	籬	䍦	蘺	䙰	魑	黐	兇	㚇	儍	猣	稯	緵	翪	朡	艐	葼	騣	鬉	鬷	鯼	匈	恟	洶	胸	詾	酗	刈	龱	囟	𡿺	惱	腦	𣬉	媲	篦	膍	貔	鎞	硇	禼	 
乂	史	吏	使	駛	更	便	哽	埂	梗	甦	硬	粳	綆	鯁	曳	拽	㹭	跩	艾	哎	砹	餀	鴱	 
𠂆	𠂋	𠀉	印	茚	䲟	襃	褎	卮	后	垢	姤	缿	詬	銗	骺	鮜	巵	梔	㐆	殷	慇	磤	𠂢	派	蒎	鎃	脈	覛	䤨	 
𠂊	祭	察	嚓	擦	䕓	鑔	漈	瘵	穄	蔡	際	豋	將	奬	槳	漿	螿	醬	𢌳	頯	炙	䍃	傜	媱	徭	愮	搖	榣	猺	瑤	窰	繇	㘥	遙	颻	鰩	鷂	䚻	㑾	䌛	 
少	劣	吵	妙	𡭝	抄	杪	沙	痧	鯊	炒	省	眇	渺	篎	省	渻	砂	秒	紗	耖	䖢	訬	鈔	雀	麨	 
尺	庹	尽	侭	咫	呎	粎	蚇	 
戊	戌	咸	喊	感	憾	撼	鱤	椷	減	瑊	箴	鱵	緘	羬	葴	諴	鍼	鹹	麙	威	崴	歲	劌	噦	濊	穢	烕	滅	戍	幾	嘰	機	璣	磯	禨	蟣	譏	鐖	鞿	饑	篾	蔑	幭	瀎	䁾	衊	襪	鱴	成	城	宬	晟	盛	誠	茂	 
丂	亏	咢	崿	愕	腭	萼	諤	遌	鄂	鍔	顎	鰐	鶚	圬	夸	侉	刳	咵	垮	姱	匏	挎	洿	瓠	摦	胯	袴	誇	跨	銙	骻	肟	雩	嫮	樗	謣	兮	盻	号	號	饕	呺	枵	鴞	粤	巧	朽	甹	俜	娉	聘	騁	羲	曦	犧	考	拷	栲	烤	銬	 
乜	也	㐌	拖	柂	胣	袘	迤	他	怹	匜	吔	地	她	弛	扡	杝	池	灺	牠	衪	訑	貤	酏	釶	阤	馳	髢	𠬫	 
𠄎	乃	仍	夃	盈	戤	楹	奶	孕	尕	扔	朶	刴	垜	跥	躱	氖	礽	秀	琇	莠	誘	透	鼐	 
亡	匄	吂	妄	侫	巟	荒	塃	慌	謊	忘	莣	忙	望	杗	杧	氓	汒	茫	牤	𤣴	盲	罔	惘	網	輞	芒	硭	鋩	蝱	衁	 
乞	仡	吃	屹	忔	扢	杚	汔	疙	籺	紇	訖	迄	齕	 
亾	匃	曷	偈	喝	愒	揭	暍	楬	歇	蠍	渴	猲	碣	竭	葛	蝎	褐	謁	藹	靄	謁	遏	鞨	餲	鶡	 
㐄	年	夅	佭	洚	䂫	絳	降	 
夬	决	吷	快	筷	抉	決	炔	玦	缺	袂	觖	訣	趹	駃	鴂	鴃	 
五	伍	吾	唔	圄	悟	捂	敔	晤	梧	焐	牾	痦	衙	語	鼯	 
㠯	𠂤	師	獅	篩	帥	追	遣	譴	搥	槌	㷟	縋	膇	鎚	佀	官	倌	婠	棺	涫	琯	痯	管	綰	菅	輨	逭	錧	館	耜	 
穵	挖	 
丁	仃	亭	停	楟	渟	聤	葶	厅	叮	可	哥	歌	何	荷	哿	呵	奇	倚	剞	埼	寄	崎	徛	掎	攲	椅	欹	猗	漪	琦	碕	綺	觭	踦	輢	錡	騎	柯	河	珂	疴	砢	笴	舸	苛	訶	軻	阿	啊	娿	屙	宁	佇	咛	紵	羜	貯	打	咑	朾	汀	町	疔	寧	儜	擰	濘	獰	薴	盯	訂	酊	釘	靪	頂	飣	 
丩	丱	𢇇	聯	關	収	叫	收	荍	朻	㽱	糾	虯	觓	訆	 
𠂈	𠂎	𠂑	卯	卵	毈	㲉	孵	乮	卿	奅	𣶐	峁	昴	柳	泖	聊	茆	鉚	留	塯	廇	㨨	籀	榴	溜	熘	瘤	罶	蹓	遛	镏	霤	飀	餾	騮	貿	𨥫	劉	懰	瀏	亥	侅	刻	劾	咳	垓	孩	峐	晐	核	欬	氦	畡	硋	絯	胲	荄	該	豥	𨀖	閡	陔	頦	䬵	駭	骸	 
了	亨	哼	烹	 
𠄐	予	豫	序	抒	杼	紓	芧	野	墅	預	 
于	吁	冔	圩	宇	旴	杅	汙	玗	盂	盱	竽	紆	芋	訏	迂	 
𠂌	乎	呼	烀	虖	嫭	罅	 
戉	狘	越	樾	𧑅	鉞	魆	 
三	丰	彗	嘒	慧	槥	熭	篲	轊	㓞	契	揳	楔	猰	瘈	禊	鍥	㛃	恝	挈	栔	絜	潔	齧	害	割	嗐	搳	犗	瞎	豁	轄	鎋	夆	埄	峯	烽	蜂	逢	篷	縫	蓬	鋒	憲	幰	玤	砉	騞	肨	蚌	邦	梆	綁	𡗗	春	惷	椿	踳	鬊	鰆	泰	傣	秦	榛	臻	蓁	螓	轃	舂	憃	摏	樁	仨	段	塅	椴	碫	緞	鍛	弎	 
𠀆	丮	奉	俸	唪	捧	棒	琫	半	伴	判	叛	拌	柈	泮	牉	畔	絆	胖	袢	頖	䬳	芈	蝆	 
夫	羮	失	佚	帙	怢	抶	昳	柣	泆	瓞	眣	秩	紩	苵	蛈	袠	跌	軼	迭	镻	㚘	替	僣	潜	鐟	賛	𡂐	𩯳	輦	攆	伕	龹	券	劵	勝	卷	倦	圈	蔨	惓	捲	棬	睠	蜷	踡	鬈	𦩱	帣	幐	弮	拳	媵	賸	桊	𣳾	滕	藤	眷	絭	縢	䖭	螣	誊	豢	韏	駦	騰	齤	𦰩	嘆	暵	歎	漢	熯	艱	難	儺	戁	攤	灘	癱	臡	扶	枎	菐	僕	𡂈	纀	噗	墣	幞	撲	樸	璞	襆	蹼	轐	醭	鏷	衭	規	槻	窺	闚	趺	鈇	 
冃	冑	 
勻	均	筠	荺	鋆	昀	盷	袀	鈞	 
弍	貳	膩	 
次	佽	咨	楶	諮	姿	恣	瓷	盗	粢	茨	資	薋	餈	 
丹	雘	坍	彤	䒟	 
𠆣	㐁	 
仁	佞	 
久	匛	柩	灸	玖	疚	羑	 
仌	俎	𠧪	 
从	丛	𠅃	卒	倅	啐	崒	悴	捽	晬	𣨛	淬	焠	猝	瘁	睟	碎	窣	粹	綷	翠	臎	萃	誶	醉	顇	雜	㐺	𠈌	𠦬	众	乑	衆	聚	驟	潨	閦	僉	劒	劔	儉	劍	厱	噞	嬐	嶮	憸	撿	斂	瀲	籢	蘞	檢	歛	殮	獫	瞼	簽	臉	薟	險	顩	驗	鹼	坐	剉	座	挫	痤	矬	莝	蓌	銼	髽	夾	俠	匧	愜	篋	唊	峽	挾	梜	浹	狹	㾜	瘞	瘱	䀹	硤	筴	翜	莢	裌	鋏	頰	巫	靈	欞	筮	噬	澨	遾	覡	誣	𢓅	㦰	韱	孅	懺	櫼	殲	瀸	籤	纖	襳	讖	來	倈	勑	徠	棶	猌	憖	睞	萊	𧳟	賚	錸	騋	鯠	從	㞞	嵸	慫	摐	樅	縱	聳	豵	蹤	鏦	 
𠔿	奐	喚	換	渙	煥	 
化	华	吪	囮	杹	花	訛	貨	靴	 
付	咐	府	俯	腐	腑	弣	拊	柎	祔	符	胕	苻	蚹	跗	附	駙	鮒	䵾	 
代	岱	牮	袋	貸	蟘	黛	 
伐	垡	筏	茷	閥	 
休	咻	庥	 
伏	栿	洑	 
位	莅	蒞	 
伊	咿	 
臾	庾	瘐	腴	諛	 
𦫸	茶	嗏	搽	 
閃	㨛	 
倠	雁	䧹	應	膺	譍	鷹	 
倩	蒨	 
𠌵	鴈	贗	 
兀	𠮾	堯	僥	嘵	墝	嬈	嶢	憢	撓	曉	橈	澆	燒	磽	繞	翹	膮	蕘	蟯	襓	趬	蹺	鐃	饒	驍	髐	光	侊	恍	晃	幌	㨪	榥	桄	洸	觥	輝	銧	耀	屼	𣁋	媺	微	薇	溦	扤	杌	虺	𧈭	豗	軏	髡	 
元	刓	完	垸	寇	簆	梡	浣	烷	皖	睆	筦	羦	脘	莞	輐	院	鯇	㝴	冠	岏	忨	抏	朊	杬	玩	盶	蚖	阮	頑	魭	黿	 
允	吮	夋	俊	葰	㕙	唆	峻	悛	捘	晙	梭	浚	焌	畯	痠	皴	睃	竣	羧	脧	䘒	踆	逡	酸	陖	餕	駿	黢	 
兄	兌	兗	帨	悅	挩	梲	涗	稅	脫	莌	蛻	說	説	銳	閱	䫄	駾	鮵	党	鎲	况	呪	咒	怳	柷	況	祝	竞	競	貺	 
圥	坴	埶	勢	㙯	藝	囈	襼	摰	暬	槷	槸	熱	爇	褻	燅	䕭	睦	稑	逵	陸	夌	凌	㥄	棱	睖	稜	綾	菱	陵	鯪	 
先	侁	兟	贊	儹	囋	攢	欑	灒	瓚	纘	𧄽	讚	趲	躦	鑽	饡	毨	洗	詵	跣	酰	銑	駪	 
皃	兜	㨮	篼	蔸	貌	藐	邈	 
羌	唴	鯗	 
兒	倪	唲	掜	猊	睨	蜺	輗	霓	鬩	鯢	鶃	齯	麑	 
虎	虪	虤	贙	虒	搋	榹	篪	褫	䚦	遞	鼶	䖘	唬	彪	滮	猇	琥	甝	諕	 
竟	境	獍	糡	鏡	 
𠓜	㚒	兩	倆	啢	緉	㒼	樠	滿	懣	璊	瞞	蟎	蹣	顢	䓣	輛	 
六	帝	啻	膪	啼	揥	禘	締	蒂	諦	蹄	旁	傍	嗙	塝	榜	滂	牓	磅	耪	膀	艕	謗	鎊	髈	亦	奕	帟	弈	栾	跡	昗	冥	塓	暝	溟	瞑	螟	覭	 
介	价	妎	玠	界	疥	紒	芥	骱	齘	 
只	呮	枳	疻	䍉	軹	齞	 
𡗜	昚	尞	僚	嘹	嫽	寮	屪	藔	憭	撩	暸	橑	潦	燎	獠	療	瞭	簝	繚	膫	䕩	䜍	蹽	轑	遼	鐐	 
平	伻	匉	坪	抨	枰	泙	萍	砰	秤	苹	評	䶄	䶄	 
𦍎	業	 
內	丙	陋	㑂	㔷	柄	炳	病	鈵	吶	抐	枘	氝	汭	納	芮	焫	蚋	衲	訥	軜	鈉	 
冉	再	冓	媾	搆	斠	構	溝	篝	耩	褠	覯	講	購	遘	鞲	顜	爯	偁	稱	袡	髯	 
央	佒	奂	涣	焕	咉	坱	怏	映	殃	盎	秧	英	英	瑛	霙	鞅	鴦	 
朿	棘	僰	襋	刺	㭰	策	茦	 
龸	牚	撐	黨	儻	攩	曭	讜	钂	 
𫇦	劳	蒙	 
仒	於	唹	棜	淤	瘀	菸	閼	 
冬	咚	柊	疼	終	鼕	鼨	 
𢎥	弱	搦	溺	蒻	鰯	 
馮	凴	憑	 
亢	伉	匟	吭	坑	抗	杭	沆	炕	犺	秔	肮	骯	航	蚢	迒	鈧	閌	頏	魧	 
冗	壳	殻	慤	沉	 
秃	痜	鋵	頽	 
凸	𠱂	 
凹	兕	 
凷	屆	 
出	咄	屈	倔	𠜾	堀	崛	掘	淈	窟	䓛	䘿	镼	拙	朏	祟	窋	粜	糶	絀	茁	詘	貀	黜	 
𨊥	𣪠	墼	擊	繫	蘻	罊	轚	 
分	份	吩	坋	坌	𣴞	岔	忿	扮	掰	攽	肦	棼	枌	氛	玢	瓰	盆	湓	葐	盼	竕	粉	彜	紛	羒	芬	棻	貧	邠	酚	雰	頒	寡	魵	鼢	 
叧	拐	 
𠠴	劦	協	勰	栛	珕	脅	嗋	荔	 
加	乫	伽	咖	妿	架	枷	珈	痂	笳	耞	𦙲	瘸	茄	嘉	賀	跏	迦	鉫	駕	 
另	柺	 
务	務	霧	 
男	嬲	娚	甥	舅	虜	擄	 
𦉶	蜀	噣	擉	歜	濁	燭	獨	臅	蠋	襡	觸	躅	鐲	韣	鸀	 
北	丠	乖	㼱	乘	剩	騬	背	偝	 
它	佗	咜	坨	柁	沱	砣	紽	舵	蛇	酡	鉈	陀	駝	鮀	鴕	 
㫐	𡬠	爵	嚼	灂	爝	皭	釂	 
皀	卽	喞	堲	節	櫛	癤	鯽	旣	嘅	墍	摡	槪	漑	蔇	朗	𣪘	廏	 
𠤑	彘	 
頃	傾	廎	㯋	熲	穎	顈	䔛	 
叵	𣲳	笸	鉕	 
巨	乬	佢	岠	拒	柜	歫	洰	渠	蕖	炬	矩	秬	粔	苣	蚷	詎	距	鉅	駏	 
匝	咂	㧜	箍	砸	鉔	 
匡	劻	哐	恇	框	眶	筐	誆	 
匪	榧	篚	 
匹	甚	勘	墈	磡	堪	嵁	戡	揕	斟	椹	湛	煁	碪	糂	葚	諶	踸	黮	苉	鴄	 
医	悘	嫕	殹	嫛	瞖	繄	翳	醫	鷖	黳	 
卄	龷	𠀗	𤰇	備	憊	鞴	韛	共	其	㐞	倛	基	璂	娸	惎	斯	凘	嘶	廝	撕	澌	𤺊	蟴	期	棋	欺	琪	𤿺	簸	碁	祺	箕	綦	萁	諆	䫏	騏	魌	麒	供	典	㥏	捵	碘	腆	覥	哄	𡱒	殿	臀	澱	癜	巽	僎	噀	撰	簨	譔	選	饌	巷	港	恭	拱	拲	謈	栱	㳟	暴	儤	曝	瀑	爆	犦	襮	洪	篊	烘	珙	異	冀	驥	廙	戴	糞	瀵	翼	瀷	蛬	谼	輂	檋	鬨	䳍	曲	䒼	曹	嘈	慒	槽	漕	糟	艚	螬	蹧	遭	蛐	豊	澧	𧰟	禮	醴	體	鱧	農	儂	噥	憹	濃	㺜	穠	膿	襛	譨	醲	齈	華	曄	曅	爗	燁	譁	鏵	韡	畢	縪	蓽	蹕	韠	𠦒	展	搌	碾	蹍	輾	昔	借	剒	厝	唶	惜	措	斮	腊	棤	皵	碏	䄍	耤	籍	藉	蜡	䜺	踖	醋	錯	鵲	散	撒	鏾	霰	饊	卌	無	幠	廡	憮	撫	甒	膴	舞	蕪	冊	刪	𠕁	侖	倫	掄	棆	淪	㷍	睔	綸	論	輪	㕟	嗣	扁	偏	㓲	匾	徧	惼	楄	煸	碥	篇	編	翩	艑	萹	褊	諞	遍	騙	鯿	 
千	仟	扦	瓩	竏	重	動	慟	尰	揰	湩	瘇	種	腫	董	懂	衝	踵	鍾	釺	阡	熏	勳	壎	曛	燻	纁	臐	薰	醺	 
卂	巩	汛	煢	籸	𦟀	嬴	瀛	臝	羸	蠃	贏	籯	鸁	訊	迅	 
仐	傘	 
午	啎	仵	忤	杵	許	滸	迕	 
𠤏	駂	鴇	 
夲	皋	嗥	皞	 
早	𠦝	乹	乾	倝	幹	擀	簳	斡	榦	翰	瀚	螒	雗	鶾	戟	朝	嘲	廟	潮	卓	倬	啅	悼	掉	淖	綽	罩	趠	踔	逴	鵫	草	騲	覃	撢	潭	燂	瞫	簟	蕈	贉	醰	鐔	 
𠦂	率	摔	繂	皐	嘷	槹	翺	 
卑	俾	埤	婢	庳	螷	捭	椑	顰	牌	簰	猈	痺	碑	稗	箄	粺	綼	脾	萆	蜱	裨	陴	鞞	髀	鵯	鼙	 
隼	凖	榫	 
章	傽	嶂	幛	彰	樟	璋	瘴	贛	戇	障	麞	 
下	丐	丏	𡧍	沔	眄	麪	鈣	卞	忭	抃	汴	吓	芐	 
卝	㐀	 
𠬝	服	箙	鵩	赧	 
仄	昃	 
厃	危	佹	垝	恑	桅	脆	詭	跪	頠	鮠	詹	儋	噡	幨	憺	擔	檐	澹	甔	瞻	簷	膽	舚	薝	蟾	襜	譫	贍	韂	黵	 
厄	呃	扼	苊	蚅	阨	軛	 
反	扳	鋬	板	版	畈	眅	粄	販	返	鈑	阪	飯	魬	 
屵	岸	 
厘	喱	甅	竰	糎	 
么	仫	吆	簒	麽	 
云	侌	陰	廕	癊	蔭	会	伝	凨	抎	沄	紜	耘	芸	雲	曇	壜	澐	魂	 
𠫓	充	統	銃	𡿮	梳	流	鎏	琉	䟽	疏	蔬	硫	酼	醯	鋶	弃	育	堉	徹	撤	澈	轍	 
公	伀	妐	松	凇	崧	菘	鬆	翁	塕	滃	蓊	衮	滚	磙	蓘	訟	頌	 
厸	厽	亝	絫	㒍	晉	戩	搢	瑨	縉	 
去	丟	銩	刼	厾	佉	刦	劫	却	呿	弆	怯	抾	法	盍	嗑	搕	榼	溘	瞌	磕	蓋	壒	闔	饁	祛	胠	袪	朅	 
叉	㕚	蚤	慅	搔	瘙	糔	騷	鰠	鼜	扠	杈	汊	衩	釵	靫	 
𠬛	沒	 
双	叒	叕	剟	啜	惙	掇	棳	畷	綴	罬	裰	輟	醊	歠	錣	餟	桑	嗓	搡	磉	顙	 
𠬢	弢	 
𠬪	受	授	綬	 
隻	㨦	䉟	蒦	劐	嚄	擭	檴	濩	獲	矱	穫	臒	艧	蠖	護	鑊	𩟓	鱯	 
𠮛	司	伺	祠	笥	詞	飼	同	侗	峒	恫	戙	桐	洞	痌	硐	筒	胴	衕	酮	銅	鮦	嘼	獸	畐	偪	冨	副	匐	蔔	堛	富	幅	愊	楅	湢	煏	福	腷	葍	蝠	輻	逼	睘	儇	圜	嬛	寰	懁	𢩠	𣟴	擐	澴	環	繯	翾	蠉	轘	還	鐶	闤	鬟	䴉	事	倳	剚	 
㕣	簭	冏	矞	劀	噊	橘	氄	潏	燏	獝	繘	譎	遹	鐍	霱	鱊	鷸	商	墒	熵	裔	雟	沿	船	鉛	 
冋	向	嚮	晌	餉	坰	喬	毊	僑	嘺	嬌	嶠	𢕪	屩	撟	敽	橋	獢	䀉	矯	簥	繑	蕎	䚩	趫	蹻	轎	驕	鷮	尚	堂	樘	瞠	膛	螳	蹚	鏜	鞺	常	掌	礃	敞	厰	廠	氅	淌	當	劏	噹	壋	擋	檔	璫	簹	蟷	襠	緔	耥	賞	償	趟	䠀	躺	䣊	扃	泂	炯	絅	詗	迥	駉	尙	倘	 
召	㲈	佋	劭	卲	岧	弨	怊	招	昭	照	沼	炤	笤	紹	苕	詔	貂	超	軺	迢	鞀	韶	髫	齠	 
𠮥	毚	儳	劖	嚵	巉	攙	欃	瀺	纔	讒	鑱	饞	免	兔	冤	蒬	堍	菟	冕	俛	凂	勉	娩	嬎	㝃	悗	挽	晚	浼	絻	輓	逸	鞔	鮸	㲋	𤟭	象	像	橡	蟓	 
句	佝	劬	呴	喣	拘	斪	昫	煦	枸	欨	狗	竘	蒟	笱	絇	翑	耈	胊	苟	敬	儆	擎	檠	蟼	警	驚	袧	軥	鉤	雊	駒	鼩	齁	齣	 
古	估	克	𠒐	𠒘	兝	剋	兛	兙	𠓏	兣	𠓎	兢	𠒲	𠒙	殑	兞	氪	兡	𠒭	𠓈	𪞎	啇	嘀	嫡	摘	敵	樀	滴	謫	豴	蹢	適	擿	鏑	咕	固	個	嗰	凅	堌	婟	崮	涸	痼	箇	錮	姑	菇	嘏	居	倨	啹	据	椐	琚	腒	裾	踞	鋸	岵	怙	故	做	枯	沽	牯	𪻕	祜	罟	胡	湖	煳	糊	葫	餬	鬍	瑚	苦	楛	蛄	詁	軲	辜	酤	鈷	骷	 
占	乩	佔	呫	坫	帖	萜	店	惦	掂	踮	怗	扂	拈	沾	霑	玷	痁	砧	站	笘	粘	苫	覘	貼	跕	阽	䩞	颭	鮎	黇	黏	點	 
叩	命	 
台	乨	佁	冶	咍	始	怠	䈚	怡	抬	枱	殆	治	箈	炱	瓵	眙	笞	紿	胎	苔	詒	貽	跆	迨	飴	駘	鮐	齝	 
叹	亟	極	殛	 
吅	𠁁	斲	鬬	喪	咒	品	區	傴	剾	嘔	奩	嫗	嶇	彄	慪	摳	樞	歐	毆	漚	甌	瞘	蓲	櫙	謳	貙	軀	䧢	饇	驅	鷗	㗊	嘂	器	噩	嚚	囂	嵒	癌	喿	噪	操	澡	藻	燥	璪	繰	臊	譟	躁	榀	碞	𠱠	霝	櫺	蘦	醽	𪋶	𠽽	斝	啙	哭	㽞	單	僤	匰	囅	嘽	墠	彈	憚	戰	撣	殫	潬	燀	癉	磾	禪	簞	繟	蕇	蘄	玂	蟬	襌	觶	䡲	闡	驒	辴	鼉	𨾴	雚	勸	嚾	𢑆	虇	懽	權	歡	灌	爟	瓘	矔	罐	蠸	觀	讙	貛	顴	驩	鸛	鑵	駡	 
吕	呂	侶	宮	梠	營	瀯	筥	莒	鋁	閭	櫚	丳	 
𠮷	周	倜	凋	啁	彫	惆	琱	碉	禂	稠	綢	蜩	裯	調	賙	輖	週	雕	鯛	鵰	洁	袁	園	榬	猿	轅	遠	 
吉	㐖	佶	㓤	劼	咭	姞	拮	桔	洁	硈	秸	結	聐	臺	儓	擡	檯	薹	蛣	袺	詰	頡	擷	纈	襭	髻	鮚	黠	䕸	 
各	㗉	咯	客	喀	揢	額	髂	恪	挌	格	洛	落	烙	珞	略	撂	硌	絡	胳	茖	袼	觡	詻	貉	賂	路	潞	璐	鏴	露	鷺	輅	簵	酪	鉻	閣	擱	雒	頟	駱	骼	鮥	鵅	 
名	眳	茗	酩	銘	 
吋	壽	儔	壔	幬	檮	濤	燾	疇	禱	籌	翿	譸	鑄	魗	 
戓	或	國	嘓	幗	摑	槶	膕	蟈	域	彧	惑	棫	淢	䈅	緎	罭	蜮	馘	魊	䱛	 
吝	麐	 
杏	莕	 
束	柬	揀	楝	湅	煉	練	萰	諫	鍊	闌	闌	攔	欄	瀾	爛	籣	蘭	糷	韊	襴	讕	鰊	剌	喇	揦	勅	𠲿	悚	敕	嫩	梀	𣒛	欶	嗽	漱	簌	蔌	遬	竦	綀	賴	懶	瀨	獺	癩	籟	藾	踈	辣	速	頼	餗	駷	 
吿	俈	晧	梏	浩	牿	皓	澔	窖	誥	造	簉	糙	䎭	酷	鋯	靠	鵠	 
咅	倍	剖	培	掊	敨	棓	殕	焙	瓿	碚	稖	䎧	菩	賠	踣	部	篰	蔀	醅	錇	闇	陪	鞛	 
君	宭	唐	傏	塘	搪	溏	煻	瑭	糖	螗	赯	醣	餹	捃	涒	焄	珺	窘	羣	群	莙	裙	郡	頵	麏	 
哀	衰	榱	縗	蓑	偯	鎄	 
軎	毄	 
唯	鷕	 
中	𠀐	貴	匱	櫃	圚	憒	樻	殨	潰	瞶	簣	繢	聵	蕢	𧑋	遺	壝	鐀	闠	隤	靧	鞼	饋	𠂝	禹	瑀	萭	齲	仲	冲	㕜	叓	串	患	賗	婁	僂	嘍	塿	寠	屢	屨	嶁	廔	慺	摟	數	擻	籔	藪	樓	漊	瘻	瞜	窶	簍	縷	𧃒	耬	膢	艛	蔞	螻	褸	䝏	貗	鏤	髏	䱾	忠	忡	沖	盅	翀	衷	馽	 
囚	𢘄	泅	𥁕	嗢	媼	慍	搵	榲	溫	熅	瘟	縕	蘊	膃	蒕	豱	轀	醞	韞	鰮	 
四	囧	呬	𧶠	匵	櫝	殰	瀆	牘	犢	竇	續	藚	覿	讀	讟	贖	韇	黷	怬	愣	柶	楞	泗	駟	 
回	㐭	啚	圖	鄙	禀	稟	凜	廩	懍	檁	澟	嗇	嬙	廧	檣	牆	蘠	穡	薔	轖	佪	徊	洄	茴	蛔	迴	 
因	咽	姻	恩	嗯	摁	蒽	氤	洇	烟	絪	胭	茵	裀	銦	駰	 
囙	卣	逌	 
困	悃	捆	梱	睏	稇	閫	 
囷	稛	箘	菌	蜠	麕	 
圂	慁	溷	 
圍	潿	 
𡈼	𢽠	徵	懲	廷	庭	挺	梃	珽	筳	綎	脡	艇	莛	𨉈	鋌	霆	鼮	 
𡉀	廛	纏	躔	 
圣	怪	 
圭	佳	刲	卦	啩	掛	罫	褂	厓	啀	娾	崖	捱	涯	𤦐	睚	哇	垚	奎	喹	蝰	娃	封	葑	鞤	恚	桂	溎	洼	窪	烓	畦	眭	硅	絓	罣	茥	蛙	街	袿	詿	跬	閨	鞋	鮭	䵷	 
坊	塄	 
坎	莰	 
坄	毀	檓	燬	譭	 
坒	梐	陛	 
𥤧	竈	 
芏	倕	垂	厜	唾	埵	捶	棰	甀	睡	箠	菙	諈	郵	錘	陲	 
垔	堙	湮	甄	籈	薽	禋	諲	闉	 
堇	僅	勤	懃	厪	墐	廑	慬	槿	殣	瑾	螼	覲	謹	饉	 
墨	纆	 
壬	任	凭	恁	荏	賃	妊	㸒	婬	淫	霪	紝	聽	廳	衽	飪	 
処	處	 
处	咎	晷	厬	櫜	綹	鯦	鼛	麔	昝	偺	喒	揝	糌	 
𢖻	愛	僾	噯	嬡	曖	璦	薆	鑀	 
𪊎	慶	 
夗	宛	剜	啘	婉	帵	惋	惌	涴	琬	畹	碗	腕	菀	蜿	踠	鵷	黦	怨	㼝	眢	苑	鴛	 
多	侈	𠛫	夠	哆	奓	恀	栘	爹	移	簃	鉹	黟	 
𡿪	拶	 
天	奏	揍	湊	腠	輳	关	眹	𦨶	送	吞	吴	俣	娱	昊	癸	戣	揆	暌	湀	睽	葵	闋	祆	𦬞	蚕	龑	 
夭	仸	㕭	呑	妖	忝	掭	添	舔	殀	沃	鋈	祅	穾	笑	訞	飫	䴠	 
旲	莫	募	嗼	墓	寞	幕	冪	慔	慕	摹	暮	模	漠	瘼	瞙	膜	蟆	謨	貘	饃	䮬	 
美	渼	鎂	 
耎	偄	渜	輭	餪	 
䙲	䙴	𢳍	遷	 
奴	伮	努	呶	孥	帑	弩	怒	怓	砮	笯	駑	 
如	帤	恕	挐	洳	絮	茹	袽	銣	鴽	 
奻	姦	 
好	孬	 
安	咹	按	晏	騴	案	桉	氨	胺	銨	鞍	頞	 
妟	匽	偃	堰	揠	蝘	鰋	鶠	宴	 
妥	挼	桵	綏	荽	餒	 
委	倭	捼	𣨙	痿	矮	緌	萎	諉	踒	逶	餧	魏	巍	犩	 
妾	唼	接	椄	翣	霎	𩸬	 
要	喓	腰	葽	𧍔	騕	 
孔	吼	犼	芤	 
孖	孨	孱	僝	潺	轏	驏	孴	 
字	牸	 
㫗	厚	 
孚	乳	俘	桴	殍	浮	烰	稃	粰	罦	脬	莩	郛	 
孤	菰	 
季	悸	 
孝	哮	教	嘋	痚	酵	 
寺	侍	峙	庤	待	偫	恃	持	時	塒	蒔	特	畤	痔	等	㩐	詩	鼭	 
守	狩	 
寻	尋	噚	撏	潯	燖	蕁	鱘	 
寽	埒	捋	酹	 
辱	媷	薅	溽	縟	耨	蓐	褥	 
尒	伱	苶	 
尔	你	您	 
𣌢	𡮂	𡭽	𧈅	𨻶	亰	 
尤	优	尨	厖	哤	牻	蛖	駹	沋	疣	𥝴	嵇	稽	訧	 
𡯄	拋	 
𠃜	声	殸	磬	罄	聲	謦	鏧	馨	眉	堳	媚	楣	湄	猸	鎇	鶥	 
𡰥	叚	假	暇	椵	犌	瑕	瘕	葭	蝦	豭	𨉣	遐	蕸	霞	騢	鰕	麚	 
尼	伲	呢	妮	昵	柅	泥	痆	鈮	 
𡰪	辟	僻	劈	壁	嬖	幦	擗	擘	檗	澼	璧	甓	癖	糪	繴	臂	薜	襞	譬	躃	避	鐾	闢	霹	 
𡰲	𣐺	 
𡰯	刷	唰	涮	 
𡰸	屐	 
尾	娓	𤈦	 
尿	屬	囑	斸	欘	矚	钃	脲	犀	墀	樨	遲	 
屋	偓	剭	喔	幄	握	楃	渥	腛	齷	 
屖	稺	 
屚	漏	瘺	 
屰	㖾	遻	朔	嗍	塑	愬	搠	槊	溯	蒴	欮	厥	劂	噘	嶡	憠	撅	橛	蕨	蟨	蹶	蹷	鐝	鱖	鷢	瘚	闕	逆	 
仚	佡	 
𡵲	黴	 
岡	剛	崗	掆	犅	綱	鋼	 
島	搗	 
仝	砼	 
式	拭	栻	試	軾	 
空	倥	悾	控	腔	鞚	 
差	傞	嗟	搓	槎	瑳	瘥	磋	艖	蒫	蹉	鹺	齹	 
項	澒	 
巴	𠂬	𠈊	㛂	吧	㞎	岊	岜	帊	弝	把	筢	杷	爬	爸	疤	皅	葩	笆	羓	耙	肥	淝	萉	蜰	芭	蚆	豝	鈀	靶	䶕	 
包	刨	咆	庖	抱	菢	枹	泡	炮	炰	狍	皰	砲	胞	苞	袍	跑	鉋	雹	鞄	飽	骲	鮑	齙	麅	 
帀	鳾	 
市	市	柿	沛	霈	肺	鬧	 
凧	佩	珮	 
吊	屌	 
帛	幫	棉	緜	綿	錦	 
芇	繭	襺	 
𢆉	南	喃	罱	腩	蝻	幸	執	墊	摯	縶	蟄	褺	贄	騺	鷙	倖	報	啈	圉	婞	悻	𪯎	盩	盭	涬	睪	凙	圛	𢋇	懌	擇	籜	蘀	斁	檡	澤	繹	襗	譯	醳	釋	鐸	驛	丵	𣪲	𣫞	鑿	叢	 
幵	幷	倂	屛	𠌸	摒	甁	腁	荓	輧	逬	餠	騈	骿	姸	汧	研	筓	豣	趼	 
旱	垾	悍	捍	桿	焊	睅	稈	趕	駻	 
幼	呦	坳	怮	拗	窈	袎	靿	黝	 
𢆶	𢆸	㡭	斷	籪	𦇓	幽	畿	𢇁	㬎	㬤	濕	隰	韅	顯	兹	孳	嵫	慈	滋	磁	茲	嗞	孶	甆	鰦	 
𨙵	鄕	曏	膷	蠁	響	饗	 
康	槺	糠	鏮	 
廆	䕇	 
廣	壙	彍	懭	擴	曠	櫎	瀇	獷	礦	穬	纊	 
建	健	揵	楗	毽	犍	腱	鍵	鞬	騝	 
开	并	倂	姘	拼	絣	鉼	刑	侀	型	硎	鉶	妍	形	枅	汧	䓑	研	揅	茾	荆	鈃	開	雃	𪊑	 
升	呏	昇	竔	阩	陞	 
卉	奔	枿	賁	僨	噴	墳	幩	憤	濆	羵	蕡	蟦	豶	轒	饙	鱝	𪎰	鼖	 
弁	弆	拚	昪	閞	 
戒	悈	械	祴	裓	誡	駴	 
弄	㟖	筭	 
舁	與	嶼	舉	藇	譽	鱮	興	舋	亹	釁	爂	爨	璺	輿	 
引	吲	矧	紖	蚓	鈏	靷	 
弘	泓	強	犟	繈	膙	襁	鏹	鞃	 
夷	侇	咦	姨	桋	洟	痍	眱	胰	荑	 
弜	弼	粥	鬻	 
弭	渳	葞	麛	 
雋	儁	㝦	鐫	 
互	仾	冱	魱	 
刍	急	煞	 
疌	倢	啑	寁	捷	睫	箑	踕	 
雪	鱈	 
㐱	參	慘	摻	槮	滲	瘮	磣	穇	篸	糝	縿	襂	驂	鬖	鰺	黲	抮	殄	餮	沴	珍	畛	疹	眕	紾	翏	僇	勠	嫪	寥	憀	戮	摎	樛	漻	璆	疁	瘳	繆	膠	蓼	謬	豂	醪	鏐	飂	鷚	胗	袗	診	趁	跈	軫	 
須	嬃	鬚	 
役	垼	 
律	葎	 
必	咇	宓	密	蜜	怭	柲	毖	泌	瑟	璱	珌	秘	苾	䛑	謐	鉍	閟	䪐	飶	馝	駜	鮅	 
𠇍	叅	隳	 
志	痣	誌	鋕	 
忌	誋	跽	 
忒	鋱	 
𢗰	惢	橤	繠	蕊	 
思	偲	崽	㩄	揌	緦	葸	慮	勴	攄	濾	藘	鑢	䚡	諰	鍶	顋	颸	鰓	 
息	媳	熄	瘜	憩	蒠	螅	鎴	 
恬	湉	 
悶	燜	 
惟	罹	 
意	億	噫	憶	檍	繶	臆	薏	醷	鐿	 
㥑	憂	優	嚘	懮	擾	櫌	瀀	獶	纋	耰	 
𢦏	哉	栽	胾	臷	蛓	裁	載	酨	截	蠘	 
戔	俴	剗	帴	棧	殘	淺	琖	盞	箋	賤	濺	踐	醆	錢	餞	 
戹	呝	豟	軶	阸	 
启	倉	傖	凔	創	嗆	愴	戧	搶	槍	滄	熗	牄	瑲	瘡	艙	蒼	螥	蹌	鎗	鶬	啟	𨐙	薛	孽	蘖	糵	 
𢼄	啓	棨	綮	肇	𦜑	 
所	乺	 
戾	㑦	唳	捩	淚	綟	䓞	 
扇	搧	煽	謆	䥇	騸	 
肩	掮	顅	 
扈	槴	滬	 
雇	僱	顧	 
扣	筘	 
我	俄	哦	娥	峨	睋	硪	義	儀	艤	蟻	議	轙	莪	蛾	鋨	餓	騀	鵞	 
𢪒	搿	 
技	庪	 
折	乴	哲	晢	晣	浙	狾	硩	䇽	蜇	誓	踅	逝	 
抓	摇	 
拑	箝	 
拍	啪	 
拉	啦	 
㧮	揑	 
推	蓷	 
𥄎	敻	瓊	藑	觼	闅	 
虔	榩	 
斥	坼	拆	柝	泝	蚸	訴	跅	 
斦	質	懫	櫍	礩	躓	鑕	 
欣	掀	𣔙	焮	鍁	 
㫃	旃	施	𠷇	箷	葹	䗐	旝	旐	旗	斿	游	遊	旆	旂	旜	𣄙	旄	旅	膂	旊	旌	旋	漩	璇	鏇	族	嗾	瘯	簇	蔟	鏃	旓	旟	旞	旒	 
放	倣	敖	傲	嗷	廒	摮	熬	獒	璈	聱	蔜	𧑃	謷	贅	遨	鏊	䮯	鰲	鼇	敷	敫	儌	噭	徼	撽	檄	激	獥	皦	礉	竅	繳	薂	覈	譥	邀	 
电	奄	俺	剦	唵	埯	庵	掩	晻	淹	罨	腌	菴	醃	閹	黤	電	 
旬	侚	徇	恂	惸	栒	殉	洵	眴	筍	絢	荀	詢	迿	 
旨	嘗	嚐	鱨	𥠻	恉	指	脂	詣	酯	䭫	鮨	𪊨	 
明	盟	萌	 
東	凍	腖	棟	氭	涷	陳	蔯	鶇	 
昏	婚	惛	殙	痻	閽	 
沓	誻	踏	錔	 
者	偖	堵	奢	𠍽	奲	屠	暑	楮	渚	煮	瘏	箸	緖	署	曙	薯	翥	著	𤏸	躇	褚	覩	觰	諸	儲	櫧	藷	豬	瀦	賭	赭	都	嘟	鍺	闍	陼	 
耆	嗜	搘	榰	蓍	鬐	鰭	 
魯	嚕	擼	櫓	穭	鑥	 
昌	倡	𠭒	唱	娼	猖	菖	錩	閶	鯧	 
書	圕	 
刖	俞	偷	喻	前	剪	㡐	揃	湔	煎	翦	譾	騚	鬋	葥	箭	 
朋	倗	堋	崩	嘣	繃	蹦	弸	掤	棚	硼	萠	蒯	輣	鬅	鵬	 
閒	僩	嫺	撊	㵎	癇	瞯	𥳑	襉	覵	鐗	鬜	鷳	 
朮	怵	秫	術	訹	述	鉥	 
札	紮	蚻	 
呆	楶	保	堡	煲	緥	葆	棠	枲	葈	 
析	唽	晰	淅	皙	菥	蜤	蜥	 
杲	桌	 
林	冧	啉	𡘽	婪	漤	彬	惏	森	淋	焚	棥	樊	攀	襻	礬	蠜	琳	楚	儊	憷	濋	礎	齼	楙	禁	噤	襟	鬱	菻	霖	麓	 
𣏟	㪔	𢽳	潸	 
采	啋	寀	彩	採	睬	綵	菜	踩	 
某	媒	煤	禖	謀	 
果	倮	彙	堁	夥	婐	巢	㑿	剿	勦	樔	璅	繅	罺	棵	祼	稞	窠	裸	裹	課	踝	輠	錁	顆	餜	騍	髁	 
𣐩	樂	㦡	櫟	爍	礫	藥	躒	轢	鑠	 
相	廂	想	湘	箱	緗	霜	孀	 
柔	揉	煣	猱	糅	蝚	蹂	輮	鞣	騥	 
䂞	槖	 
亲	新	薪	親	儭	嚫	櫬	襯	䞋	 
罙	探	深	琛	 
臬	甈	鎳	闑	 
桀	傑	榤	磔	 
栗	傈	凓	慄	瑮	麜	 
梄	槱	 
槀	藁	 
橫	㶇	 
正	歪	佂	整	延	埏	挻	梴	涎	筵	綖	莚	蜑	誕	鋋	鯅	征	怔	政	焉	嘕	嫣	蔫	症	罡	𧠣	竀	証	鉦	 
此	些	佌	呰	呲	庛	柴	偨	泚	玼	疵	眥	砦	紫	胔	茈	觜	嘴	訾	貲	跐	鈭	雌	骴	髭	鮆	齜	 
步	涉	陟	騭	頻	嚬	瀕	蘋	 
歨	徙	屣	縰	蓰	蹝	 
頉	夒	𡖂	 
列	例	冽	咧	栵	洌	烈	㾐	茢	裂	迾	鮤	鴷	 
死	斃	薨	屍	𢍈	葬	髒	𣨻	薧	 
𣦼	粲	璨	韰	餐	 
𩐁	薤	 
癹	發	廢	撥	橃	潑	癈	襏	鏺	 
母	每	侮	勄	毓	悔	敏	繁	蘩	鰵	晦	梅	海	嗨	痗	脢	莓	誨	酶	鋂	霉	姆	拇	 
昆	棍	混	焜	琨	䃂	緄	輥	醌	鯤	鵾	 
㲎	毳	撬	橇	竁	 
民	岷	抿	敃	愍	暋	昬	㨉	湣	緡	鍲	泯	珉	眠	笢	苠	 
畏	偎	喂	嵔	椳	渨	煨	猥	碨	腲	隈	餵	鰃	 
永	咏	昶	泳	羕	樣	漾	脉	 
氶	丞	卺	拯	烝	蒸	承	函	涵	菡	蜬	顄	𪱝	 
氽	黎	藜	桼	漆	膝	 
氾	笵	范	 
汞	銾	 
江	湼	鴻	 
彔	剝	㟤	氯	淥	盝	睩	碌	禄	綠	菉	逯	醁	錄	籙	騄	 
录	邍	 
沂	垽	 
沐	霂	 
㳄	盜	羨	檨	 
沝	淼	 
泉	灥	線	腺	䤼	鰁	 
泊	箔	 
波	婆	 
眔	瘝	褱	壞	懷	櫰	遝	嚃	鰥	 
活	闊	 
淮	匯	擓	準	 
滈	薃	 
𤆗	燕	嚥	嬿	曣	臙	讌	醼	驠	 
𤆍	𤍾	 
灵	熭	 
炎	倓	剡	㓹	罽	煔	啖	惔	掞	棪	欻	毯	氮	淡	琰	痰	睒	𦧡	菼	裧	談	錟	餤	 
炏	𤇾	勞	嘮	撈	澇	癆	耮	塋	嫈	榮	滎	熒	犖	瑩	瀅	禜	縈	瀠	罃	螢	褮	醟	鶯	燮	躞	焱	燊	 
羔	糕	 
㶳	盡	儘	孻	濜	燼	藎	贐	賮	 
焦	僬	劁	噍	樵	燋	瞧	礁	穛	蕉	譙	趭	醮	蘸	 
煩	薠	 
麃	儦	爊	皫	穮	臕	藨	鑣	 
交	佼	効	俲	咬	姣	㝔	恔	效	傚	校	洨	狡	㼎	皎	筊	絞	茭	蛟	跤	較	郊	鉸	駮	骹	鮫	 
㸚	爾	彌	瀰	獮	璽	禰	薾	邇	鸍	爽	塽	 
壯	奘	莊	裝	 
𪧇	寐	寤	寎	寢	寱	寣	 
戕	臧	藏	臟	贓	 
牟	侔	哞	眸	麰	 
牢	哰	 
狄	荻	逖	 
㹜	猋	贆	飆	 
狂	俇	誑	逛	鵟	 
狊	犑	瞁	鶪	鼳	 
突	葖	鼵	 
臭	嗅	殠	溴	糗	𨶑	 
狺	獄	嶽	 
主	住	往	暀	拄	柱	毒	注	乼	炷	疰	砫	素	傃	嗉	愫	膆	蛀	註	責	債	勣	嘖	幘	漬	磧	積	簀	績	鰿	賾	駐	黈	麈	 
全	佺	拴	栓	牷	痊	筌	荃	醛	詮	跧	輇	銓	駩	 
呈	埕	𢧜	鐵	驖	桯	珵	程	聖	檉	蟶	脭	裎	逞	酲	鋥	鞓	 
玨	班	斑	癍	琵	 
珀	碧	 
皇	偟	皝	凰	喤	徨	惶	揘	湟	煌	篁	艎	葟	蝗	遑	鍠	隍	騜	鰉	 
珤	𡩧	寶	 
㼌	窳	蓏	 
窊	搲	 
𤬦	甍	 
𣢟	嵌	 
𤯔	㚅	隆	癃	窿	 
星	惺	戥	猩	腥	醒	 
亩	畝	 
𤰔	叀	專	傳	剸	團	㩛	糰	嫥	慱	摶	漙	磚	竱	縳	轉	囀	惠	穗	繐	蕙	譓	 
备	俻	偹	 
奋	畚	 
甾	崰	疀	椔	淄	緇	菑	輜	錙	鯔	 
畜	慉	搐	滀	稸	蓄	 
畕	畺	僵	彊	疆	橿	殭	繮	薑	麠	畾	儡	壘	櫐	蘽	礧	纍	儽	欙	虆	罍	藟	鼺	 
苗	喵	媌	描	瞄	貓	錨	 
𧆨	盧	壚	廬	櫨	爐	獹	籚	纑	罏	臚	艫	蘆	蠦	鑪	顱	驢	鱸	黸	 
番	墦	審	嬸	瀋	讅	幡	播	潘	籓	藩	燔	璠	皤	磻	繙	羳	翻	膰	蕃	蟠	蹯	 
雷	擂	檑	癗	礌	蕾	鐳	 
定	淀	碇	綻	腚	錠	靛	顁	 
是	匙	媞	寔	提	𤟥	禔	緹	翨	諟	踶	醍	隄	鞮	韙	題	鯷	 
疾	嫉	槉	 
百	佰	宿	摍	縮	蹜	凮	瓸	皕	奭	𣂏	衋	竡	粨	貊	陌	 
皆	偕	喈	揩	楷	湝	稭	蒈	蝔	諧	鍇	階	 
㿟	皛	 
習	慴	摺	漝	熠	褶	霫	飁	騽	鰼	 
孟	勐	猛	錳	 
昷	温	 
泴	盥	 
𥃭	値	盾	㡒	循	楯	腯	輴	遁	 
冒	勖	媢	帽	𣔺	瑁	艒	賵	 
䀠	瞿	矍	彏	戄	攫	欔	玃	籰	蠼	貜	躩	钁	懼	癯	臞	衢	 
𥬥	算	匴	篹	篡	纂	攥	 
眯	蔝	 
敄	婺	㡔	楘	瞀	霿	蝥	鍪	騖	鶩	 
𠤕	疑	儗	凝	嶷	擬	癡	礙	碍	肄	 
矣	俟	唉	埃	娭	挨	欸	涘	誒	騃	 
知	智	蜘	踟	 
雉	薙	 
岩	啱	 
砳	磊	 
磨	礳	耱	蘑	饝	 
奈	捺	萘	 
宗	崇	悰	棕	淙	琮	粽	綜	䝋	賨	鬃	 
柰	隸	 
祘	蒜	 
票	僄	剽	嘌	嫖	幖	彯	慓	摽	標	漂	薸	熛	瓢	瞟	縹	蔈	醥	鏢	飄	驃	鰾	 
禺	偶	喁	寓	嵎	愚	耦	藕	腢	萬	勱	厲	勵	礪	糲	蠣	癘	蠆	躉	邁	遇	隅	顒	齵	 
利	俐	唎	痢	 
秋	偢	啾	㡑	愀	愁	㵞	揪	楸	甃	瞅	萩	鍫	鍬	鞦	鬏	鰍	鶖	 
秝	厤	曆	歷	嚦	櫪	瀝	癧	轣	 
昱	煜	 
竝	𤾕	 
籴	糴	 
匊	掬	椈	菊	鞠	麴	 
氣	愾	靝	餼	 
䊆	毇	 
粟	僳	 
頪	類	蘱	纇	 
系	係	孫	蓀	遜	𢾰	徽	鯀	 
糺	乿	 
紂	葤	 
紅	葒	 
累	傫	摞	縲	螺	騾	 
絲	噝	䜌	孌	孿	巒	彎	灣	戀	攣	變	欒	羉	臠	癵	蠻	鑾	鸞	𦆕	轡	 
絕	撧	蕝	 
維	濰	羅	儸	囉	攞	欏	玀	籮	蘿	邏	鑼	 
匋	掏	淘	綯	陶	 
卸	御	禦	籞	 
𦭝	夢	儚	瞢	懵	 
𦍒	達	噠	撻	澾	躂	鐽	闥	 
𦐇	塌	搨	榻	溻	褟	蹋	闒	𩌇	 
耑	喘	圌	惴	揣	湍	瑞	端	篅	貒	踹	遄	顓	 
需	儒	䨲	壖	嬬	孺	懦	擩	濡	獳	瓀	糯	繻	臑	薷	蠕	襦	轜	醹	 
耴	踂	輒	鮿	 
取	冣	娵	娶	掫	最	嘬	撮	蕞	棷	緅	菆	諏	趣	輙	陬	鯫	 
咠	戢	揖	楫	緝	葺	輯	 
耿	褧	 
聑	聶	懾	攝	欇	襵	躡	鑷	顳	 
耶	椰	爺	 
争	净	静	 
爭	凈	崢	掙	淨	猙	琤	睜	竫	箏	諍	靜	 
筆	潷	 
芛	兼	膁	傔	嗛	嫌	廉	劆	濂	簾	臁	薕	慊	搛	歉	溓	磏	縑	謙	豏	賺	鎌	隒	鰜	鶼	鼸	 
䏌	佾	 
𦘩	肸	 
肋	筋	 
䏍	能	態	熊	羆	罷	擺	䎱	藣	襬	 
肙	娟	悁	捐	涓	狷	絹	罥	蜎	鋗	鞙	駽	鵑	 
肖	俏	削	揱	箾	哨	宵	屑	榍	峭	帩	弰	悄	捎	䈰	梢	䈾	消	痟	矟	硝	稍	潲	筲	綃	艄	蛸	誚	趙	逍	銷	霄	鞘	髾	魈	 
𦘷	胤	酳	 
肯	啃	掯	 
肰	猒	厭	嚈	壓	擪	檿	厴	靨	饜	魘	然	嘫	撚	燃	 
胃	喟	媦	膚	蝟	謂	 
胥	壻	湑	稰	糈	蝑	諝	醑	 
豚	遯	 
脣	漘	 
臥	臨	監	㯺	檻	濫	礛	籃	艦	藍	襤	覽	攬	灠	爦	纜	鑑	鑒	䰐	盬	鹽	 
臤	堅	慳	䃘	鏗	鰹	掔	緊	腎	蜸	豎	賢	 
巸	媐	煕	 
𦣻	夏	嗄	廈	榎	戛	嘠	 
到	倒	捯	菿	 
致	緻	 
窒	膣	螲	 
𦥔	叟	傁	嗖	嫂	廋	搜	溲	獀	瘦	瞍	艘	謏	醙	鎪	颼	餿	 
臽	啗	掐	𢽣	欿	淊	焰	窞	蜭	諂	輡	閻	爓	陷	餡	鵮	 
臿	插	歃	牐	鍤	 
舀	慆	搯	槄	滔	稻	縚	謟	蹈	韜	䵚	 
舍	舒	倽	啥	捨	猞	騇	 
粦	粼	憐	潾	燐	甐	疄	瞵	磷	轔	辚	遴	鄰	驎	鱗	麟	 
亙	恆	堩	緪	 
般	媻	幋	搬	槃	瘢	盤	磐	縏	鞶	䰉	 
良	俍	埌	娘	悢	桹	浪	烺	狼	琅	稂	筤	簋	蜋	郎	廊	榔	郞	鋃	閬	駺	 
䖝	虱	鯴	 
虽	强	雖	 
䖵	蠚	蠭	蠢	螽	蝨	蠯	蠶	蟲	爞	蠱	蠡	劙	攭	 
衍	愆	𧍢	 
衞	讏	躛	 
表	俵	裱	錶	 
萈	寬	臗	髖	 
斛	槲	 
𧣈	解	嶰	廨	懈	澥	蟹	 
䚯	罰	 
訇	揈	渹	鞫	 
卻	腳	 
容	榕	溶	蓉	鎔	 
欲	慾	螸	 
壴	喜	嚭	僖	嘻	嬉	憙	熹	禧	蟢	譆	饎	𠷸	尌	廚	幮	櫥	樹	澍	彭	嘭	澎	甏	膨	 
豈	𧰙	豐	豔	灩	麷	凱	剴	塏	愷	榿	獃	皚	磑	覬	鎧	闓	顗	 
登	凳	噔	嶝	橙	澄	燈	瞪	磴	䆸	㡧	簦	證	蹬	鐙	 
䖒	戲	嚱	巇	 
豖	冢	啄	㞘	椓	涿	琢	瘃	諑	 
㒸	遂	檖	燧	璲	穟	邃	繸	襚	隧	隊	墜	 
家	傢	嫁	稼	鎵	 
彖	剶	劙	喙	掾	椽	瑑	祿	篆	緣	蝝	餯	 
甤	蕤	 
豙	毅	藙	 
豦	劇	噱	據	璩	臄	躆	遽	蘧	醵	鐻	 
豩	燹	 
豪	嚎	壕	檺	濠	籇	蠔	 
貇	墾	懇	 
貍	薶	霾	 
則	側	厠	崱	廁	惻	測	萴	鍘	鰂	 
負	偩	 
貞	偵	幀	楨	禎	赬	 
員	勛	圓	損	殞	溳	磒	縜	隕	霣	韻	鶰	 
𧴪	瑣	鎖	 
敗	闝	 
貫	實	慣	摜	 
買	賣	儥	凟	蕒	 
賈	價	檟	 
賏	嬰	嚶	攖	櫻	瀴	瓔	癭	纓	鸚	罌	贔	 
赦	螫	 
赫	嚇	 
射	榭	謝	麝	 
躬	窮	 
軋	錷	 
軍	㡓	惲	揮	暈	暉	楎	渾	煇	琿	皸	緷	翬	葷	褌	諢	運	韗	顐	餫	鯶	鼲	 
𨊠	範	 
斬	塹	嶄	慙	摲	暫	槧	漸	聻	魙	獑	䁪	鏨	 
䡛	轟	 
宰	滓	 
辡	辨	辦	㸤	瓣	辮	辯	 
迷	瞇	謎	醚	 
迌	遀	隨	髓	 
退	腿	褪	 
逐	蓫	 
連	僆	摙	槤	漣	璉	蓮	鏈	鰱	 
進	暹	 
道	導	 
邕	雝	廱	灉	癰	齆	 
酋	奠	鄭	擲	尊	僔	撙	樽	蹲	遵	鐏	鱒	鷷	崷	楢	猶	蕕	猷	緧	蝤	輶	遒	鞧	鰌	 
宷	奧	 
𥦓	竊	 
童	僮	噇	㠉	幢	憧	撞	曈	朣	橦	潼	犝	獞	疃	瞳	穜	罿	艟	鐘	 
欽	嶔	廞	撳	䃢	 
閔	憫	簢	 
閏	撋	潤	瞤	 
阞	泐	 
阴	隋	墮	嶞	橢	 
奞	奪	奮	 
隺	搉	榷	㿥	確	篧	蒮	鶴	 
崔	催	凗	摧	漼	璀	膗	 
翟	戳	擢	曜	櫂	濯	燿	籊	藋	趯	躍	鸐	 
萑	萑	 
𠿅	舊	 
雐	虧	 
雔	雙	𢥠	㩳	䉶	艭	犨	讎	雥	 
霍	攉	㸌	癨	矐	臛	藿	 
罪	𢶀	 
靡	劘	 
勒	嘞	鰳	 
䩗	霸	壩	 
䩻	羈	 
齏	虀	 
戠	幟	樴	熾	織	職	蘵	膱	蟙	識	 
歆	噷	 
䬕	飍	 
飤	飭	飾	 
養	瀁	癢	 
褭	㒟	㜵	 
歊	藃	 
蒿	嚆	 
鬳	獻	巘	瓛	讞	䡾	钀	齾	甗	 
鷊	虉	 
穌	蘇	 
鮮	廯	癣	蘚	 
䔡	𣩷	 
䲆	鱻	 
烏	嗚	塢	摀	歍	鎢	 
𩾏	鳳	 
廌	薦	韉	韀	 
巤	擸	臘	㯿	犣	獵	蠟	躐	鑞	鬣	鱲	 
竄	攛	躥	鑹	 
龥	籲'''

    twoRadStumps = '''一丨丄	一巛卅	一弋弌	丨一丅	丨人个	丨八丫	丨立䇂	丿刀刄	丿气氕	乙乙卍	 
                    乙尢兂	乙田乪	乙石乭	亅二亍	二二亖	二冂冄	二山亗	人力仂	人勹勽	人十什	 
                    人卜仆	人厶仏	人士仕	人夕㐴	人子仔	人山仙	人心伈	人支伎	人方仿	人比仳	 
                    人火伙	人牙伢	人牛件	人用佣	人田伸	人田佃	人白伯	人皮佊	人米侎	人羊佯	 
                    人老佬	人耳佴	人至侄	人舌佸	人舟侜	人艮佷	人血侐	人衣依	人西価	人見俔	 
                    人言信	人谷俗	人足促	人車俥	人辰侲	人里俚	人長倀	人門們	人非俳	人面偭	 
                    人韋偉	人馬傌	人鬼傀	人黽僶	人齊儕	人龍儱	儿宀宂	儿禾禿	儿高亮	八大夰	 
                    八气氘	八艸䒔	冂一𠔼	冖高䯧	冫水冰	冫金凎	冫隹准	冫靑凊	几鳥鳧	几鹿麂	 
                    凵水凼	刀艸芀	力大夯	力艸艻	匕人仑	匕勹匂	匕鹿麀	匚斤匠	匚田匣	十氏氒	 
                    十白皁	卜鳥鳪	卩丶卪	厂力历	厂干厈	厂氏𠨿	厂缶厒	厂至厔	厂非厞	厶勹勾	 
                    厶大厺	又力劝	口入叺	口八叭	口刀叨	口刀叼	口力叻	口匕叱	口十叶	口土吐	 
                    口幺吆	口心吢	口心吣	口支吱	口文呅	口斤听	口方㕫	口欠吹	口比吡	口水呇	 
                    口火吙	口牙呀	口牛吽	口犬吠	口玄呟	口瓜呱	口甘咁	口田呷	口田呻	口米咪	 
                    口耳咡	口自咱	口至咥	口艮哏	口西哂	口言唁	口貝唄	口赤哧	口走唗	口辰唇	 
                    口里哩	口金唫	口門問	口隹售	口音喑	口高嗃	口鬲嗝	口鳥鳴	口麥嘜	口麻嘛	 
                    口黑嘿	口齊嚌	口齒嚙	口龍嚨	囗又㘝	囗女囡	囗子囝	囗米𡇒	囗靑圊	土卜圤	 
                    土巛圳	土己圮	土己圯	土斤圻	土止址	土氏坁	土瓜坬	土甘坩	土田坤	土皮坡	 
                    土立垃	土羊垟	土自垍	土至垤	土艮垠	土角埆	土里埋	土阜埠	土隶埭	土隹堆	 
                    土音堷	土鬲塥	土鹿塵	土龍壟	土龍壠	夕卜外	夕食飧	大小尖	女己妃	女干奸	 
                    女戶妒	女支妓	女方妨	女比妣	女甘姏	女生姓	女田㚻	女田妯	女羊姜	女老姥	 
                    女而耍	女臣姫	女至姪	女舌姡	女辰娠	女非婓	女音㛺	女馬媽	子木李	子艸芓	 
                    寸刀刌	小齊齋	尢玉尩	尸又㞋	尸比屁	尸穴屄	尸米屎	尸非屝	山乙乢	山入屳	 
                    山山屾	山己𡵆	山气氙	山牙岈	山田岫	山田岬	山見峴	山谷峪	山隹𡹐	巛气氚	 
                    巛頁順	工力功	工卩卭	工攴攻	工老𦒳	工邑邛	己己𢀵	己攴攺	己艸芑	巾白帕	 
                    巾皮帔	巾穴帘	巾聿帇	巾長帳	巾隹帷	巾韋幃	干刀刊	干竹竿	干网罕	干門閈	 
                    干頁頇	幺乙幻	广匕庀	广支庋	广比庇	广牙庌	广田庙	广羊庠	广至庢	广車庫	 
                    广酉庮	广里㢆	广龍龐	廾己异	弓玄弦	弓瓜弧	弓穴穹	弓長張	彡丨丯	彳生徃	 
                    彳皮彼	彳艮很	彳走徒	心大忕	心寸忖	心支忮	心斤忻	心欠忺	心生性	心白怕	 
                    心羊恙	心而恧	心艮恨	心艸芯	心血恤	心西恓	心邑悒	心釆悉	心里悝	心長悵	 
                    心靑情	心非悱	心非悲	心面愐	心音愔	心鬼愧	心齊懠	戈刀划	戶己戺	戶斗戽	 
                    戶方房	戶衣扆	戶非扉	手乙扎	手八扒	手力扐	手工扛	手干扞	手戈找	手文抆	 
                    手斗抖	手曰抇	手欠扻	手止扯	手殳投	手比批	手氏扺	手田押	手田抽	手皮披	 
                    手石拓	手臣挋	手至括	手舌括	手艮拫	手角捔	手足捉	手辰振	手邑挹	手金捦	 
                    手長振	手門捫	手門閉	手非排	手音揞	手骨搰	手高搞	手鬲搹	手鹿摝	手鼻擤	 
                    手齊擠	手龍攏	支羽翅	支艸芰	支頁頍	文彡彣	文日旻	文雨雯	文非斐	文鳥鳼	 
                    斤父斧	斤艸芹	斤頁頎	方艸芳	方雨雱	日干旰	日斤昕	日方昉	日木杳	日玄昡	 
                    日玉旺	日至晊	日見晛	日門間	日靑晴	日音暗	月肉朒	木丶术	木八朳	木几凩	 
                    木力朸	木卜朴	木土杜	木大杕	木宀宋	木寸村	木山杣	木工杠	木己杞	木干杆	 
                    木弋杙	木彡杉	木手材	木支枝	木攴枚	木斗枓	木方枋	木欠杴	木比枇	木爪枛	 
                    木牙枒	木玉枉	木甘柑	木田柙	木田柚	木田柛	木白柏	木皮柀	木石柘	木而栭	 
                    木至桎	木臼桕	木舌栝	木艮根	木行桁	木見梘	木角桷	木辛梓	木里梩	木長棖	 
                    木門閑	木隶棣	木隹椎	木隹集	木非棐	木非棑	木風楓	木高槁	木髟髤	木鬲槅	 
                    木鬼槐	木鳥梟	木齊櫅	木龍櫳	欠艸芡	止人企	止几凪	止支歧	止艸芷	歹几夙	 
                    歹聿肂	歹血殈	殳艸芟	毋士毐	比竹笓	比艸芘	毛老耄	毛艸芼	毛高毫	毛髟髦	 
                    毛麻麾	水入汆	水八汃	水十汁	水夕汐	水大汏	水女汝	水山汕	水己汜	水干汗	 
                    水心沁	水日汨	水曰汩	水月㳉	水止沚	水殳没	水气汽	水犬汱	水玄泫	水玉汪	 
                    水甘泔	水田油	水田沺	水石泵	水穴泬	水立泣	水羊洋	水聿津	水自洎	水血洫	 
                    水西洒	水谷浴	水貝浿	水邑浥	水酉酒	水里浬	水金淦	水靑淸	水靑清	水面湎	 
                    水音湆	水骨滑	水魚漁	水鹵滷	水鹿漉	水黃潢	水齊濟	水龍瀧	水龠瀹	火一灭	 
                    火土灶	火巛災	火文炆	火斤炘	火日炅	火欠炊	火玄炫	火缶缹	火羊烊	火韋煒	 
                    火高熇	火齊齌	火龍爖	火龠爚	爪竹笊	爿女妝	爿斤斨	爿木牀	爿犬狀	爿羊牂	 
                    牙穴穿	牙艸芽	牙衣衺	牙邑邪	牙隹雅	牙鳥鴉	牛匕牝	牛土牡	牛攴牧	牛毛牦	 
                    牛生牲	牛田牰	牛角觕	牛高犒	牛麻犘	犬卩犯	犬干犴	犬斤㹞	犬瓜狐	犬生狌	 
                    犬田狎	犬穴狖	犬舌狧	犬艮狠	犬貝狽	犬里狸	犬靑猜	犬骨猾	玉丿玍	玉己玘	 
                    玉攴玫	玉文玟	玉月玥	玉玉珏	玉田珅	玉耳珥	玉行珩	玉見現	玉里理	玉非琲	 
                    玉韋瑋	玉鬼瑰	玉黃璜	玉龍瓏	瓜网罛	瓦十瓧	瓦毛瓱	甘弋甙	生生甡	生竹笙	 
                    生靑𩇛	田丶甶	田勹甸	田宀宙	田攴畋	田比毗	田气氠	田犬畎	田竹笛	田門閘	 
                    田鳥鴨	疒匕疕	疒山疝	疒殳疫	疒氏疧	疒火疢	疒牙疨	疒玄痃	疒甘疳	疒皮疲	 
                    疒艮痕	疒豆痘	疒里㾖	疒非痱	疒音瘖	疒風瘋	疒鬼瘣	疒黃癀	疒齊癠	白高皜	 
                    白鬼魄	皮頁頗	皮髟髲	皿疋㿿	皿禾盉	皿齊齍	目手看	目毛眊	目氏眂	目玄眩	 
                    目生眚	目穴窅	目羊着	目艮眼	目艸苜	目艸𥄕	目行䀪	目隹睢	目靑睛	目面𥈅	 
                    目鼓瞽	矛网罞	矛艸茅	矛衣袤	矛雨雺	矢豆短	石夕矽	石宀宕	石工矼	石干矸	 
                    石斤斫	石欠砍	石比砒	石牙砑	石田砷	石皮破	石西硒	石見硯	石角确	石隹碓	 
                    石頁碩	石鬼磈	石鹵磠	石黃磺	石龍礱	示土社	示己祀	示斤祈	示方祊	示止祉	 
                    示殳祋	示氏祇	示田神	示癶𥙊	示石祏	示羊祥	示見視	示邑祁	示韋禕	示馬禡	 
                    示龠禴	禾厶私	禾口和	禾山秈	禾斗科	禾比秕	禾氏秖	禾石䄷	禾隹稚	禾高稾	 
                    禾高稿	禾鹿麇	禾麻穈	禾齊穧	穴艸茓	立十竍	立毛竓	立竹笠	立羽翊	立羽翌	 
                    立艸苙	立靑靖	立風颯	立鳥鴗	米冖冞	米子籽	米宀宩	米攴敉	米斗料	米毛粍	 
                    米白粕	米立粒	米西粞	米長粻	米靑精	米鹿麋	米麻糜	糸巛紃	糸己紀	糸文紊	 
                    糸文紋	糸方紡	糸比紕	糸氏紙	糸甘紺	糸田紬	糸田細	糸田紳	糸米䋛	糸至絰	 
                    糸行絎	糸谷綌	糸豸絼	糸非緋	糸面緬	糸革緙	糸韋緯	糸高縞	糸麻縻	糸黽繩	 
                    缶工缸	羊殳羖	羊气氧	羊羽翔	羽非翡	老鳥䳓	而寸耐	而彡耏	耒子耔	耒毛耗	 
                    耳刀刵	耳心恥	耳毛毦	耳舌聒	耳艸茸	耳門闻	耳龍聾	聿禾秉	肉入肏	肉几肌	 
                    肉土肚	肉寸肘	肉工肛	肉干肝	肉彡肜	肉支肢	肉斤肵	肉殳股	肉瓜胍	肉生胜	 
                    肉田胂	肉田胄	肉田胛	肉白胉	肉示䏡	肉立𦚏	肉米脒	肉而胹	肉豆脰	肉辰脤	 
                    肉長脹	肉靑腈	肉非腓	肉面腼	肉音腤	肉高膏	肉鬲膈	肉鼓臌	肉齊臍	臣卜卧	 
                    臣宀宦	臣宀宧	臣艸茞	臣頁頣	臣頁頤	至宀室	至老耋	至至臸	至艸荎	臼衣裒	 
                    舌刀刮	舌氏舐	舌甘甜	舌竹筈	舌鳥鴰	舛艸荈	舟刀舠	舟山舢	舟工舡	舟方舫	 
                    舟玄舷	舟田舳	舟白舶	艸屮芔	艸艸茻	虫乙虬	虫工虹	虫支蚑	虫文蚊	虫斤蚚	 
                    虫毛蚝	虫父蚥	虫牙蚜	虫玄蚿	虫甘蚶	虫田䖬	虫田蚰	虫疋蛋	虫糸𫊺	虫羊蛘	 
                    虫至蛭	虫舌蛞	虫艮蛝	虫見蜆	虫辰蜃	虫阜蛗	虫隹蜼	虫非蜚	虫面蝒	虫鬼螝	 
                    虫黃蟥	虫黑蟔	虫黽蠅	虫鼓𪔖	虫龍蠪	血卩卹	血耳衈	行干衎	行玄衒	行艸荇	 
                    行金銜	行韋衛	行魚衡	行鳥鴴	衣刀初	衣彡衫	衣日衵	衣氏衹	衣玄袨	衣田袖	 
                    衣田𫋵	衣皮被	衣穴袕	衣艮裉	衣谷裕	衣豆裋	衣非裴	衣韋褘	衣鳥裊	衣龍襲	 
                    西气氥	西艸茜	見爪覓	見竹筧	見竹莧	見見覞	角力觔	角瓜觚	角黃觵	言十計	 
                    言卜訃	言寸討	言山訕	言巛訓	言工訌	言己記	言干訐	言斤訢	言方訪	言殳設	 
                    言牙訝	言皮詖	言矢䛈	言网詈	言羊詳	言羽詡	言耒誄	言舌話	言言誩	言豆䛠	 
                    言隹誰	言雨霅	言靑請	言非誹	言韋諱	言音諳	言風諷	言高謞	言黽譝	言龍讋	 
                    谷邑郤	豆支豉	豆頁頭	豸手豺	豸聿貄	豸舟貈	豸隶𧳙	貝工貢	貝弋貣	貝手財	 
                    貝辰賑	貝長賬	貝靑䝼	貝鳥鵙	貝齊齎	赤色赩	走卜赴	走山赸	走己起	走隹趡	 
                    足八趴	足支跂	足止趾	足皮跛	足石跖	足至跮	足艮跟	足西跴	足非䠊	足齊躋	 
                    足齒𪘏	車大軑	車干軒	車氏軝	車瓜軱	車田軸	車而輀	車至輊	車舟輈	車靑輤	 
                    車非輩	辛乙乵	辛艸莘	辰宀宸	辰日晨	辰雨震	辵大达	辵巛巡	辵斤近	辵牙迓	 
                    辵玉迋	辵田迪	辵白迫	辵舌适	辵言這	辵豆逗	辵隶逮	辵韋違	邑衣裛	酉寸酎	 
                    酉己配	酉干酐	酉殳酘	酉甘酣	酉禾酥	酉鬼醜	釆田釉	里衣裏	金乙釓	金乙釔	 
                    金十針	金卜釙	金口釦	金土釷	金女釹	金山崟	金巛釧	金工釭	金干釬	金弋釴	 
                    金彡釤	金方鈁	金比鈚	金火鈥	金父釜	金玄鉉	金玉鈺	金甘鉗	金田鈾	金田鈿	 
                    金田鉀	金田鉮	金白鉑	金皮鈹	金目鉬	金米銤	金老銠	金耳鉺	金至銍	金舌銛	 
                    金艮銀	金色銫	金衣銥	金西𧟴	金谷鋊	金豆鋀	金貝鋇	金辛鋅	金里鋰	金長鋹	 
                    金隹錐	金靑錆	金頁顉	金高鎬	金鬲鎘	金鹿鏖	金龠鑰	長大套	長聿肆	門一閂	 
                    門方閍	阜方防	阜止阯	阜皮陂	阜艮限	阜走陡	阜車陣	阜鬲隔	阜鬼隗	阜齊隮	 
                    阜龍隴	靑气氰	靑竹箐	靑艸菁	靑鳥鶄	非刀剕	非艸菲	非雨霏	面力勔	面見靦	 
                    革斤靳	革皮鞁	革禾鞂	革艮鞎	韋艸葦	韋長韔	韋門闈	音穴窨	風山嵐	風舌颳	 
                    食几飢	食欠飮	食耳餌	食舌餂	食虫蝕	食豆餖	食非餥	食鬼餽	香非馡	香麻黁	 
                    馬又馭	馬大馱	馬巛馴	馬日馹	馬爻駁	馬艸䔍	馬辛騂	馬門闖	馬隹騅	馬非騑	 
                    馬風颿	馬鬼騩	骨干骭	骨殳骰	骨鳥鶻	高山嵩	高攴敲	高日暠	高竹篙	高羽翯	 
                    鬲羽翮	鬲艸蒚	鬲虫融	鬼山嵬	鬼彡鬽	鬼支鬾	鬼斗魁	鬼艸蒐	鬼衣褢	鬼隹魋	 
                    鬼麻魔	魚刀魛	魚己魢	魚方魴	魚比魮	魚而鮞	魚里鯉	魚靑鯖	魚非鯡	魚黃鱑	 
                    魚黽鱦	鳥乙鳦	鳥弋鳶	鳥穴窵	鳥穴鴥	鳥竹䉆	鳥艸蔦	鳥隹鵻	鹵艸蓾	鹿竹簏	 
                    鹿邑鄜	麻手𪎚	麻艸蔴	黃竹簧	黑犬默	黑甘黚	黑音黯	黑黽䵴	黽丶𪓑	鼎冖鼏	 
                    鼎手鼒	鼠文鼤	鼠犬鼣	鼠生鼪	鼠田鼬	鼠石鼫	鼠隹䶆	鼠靑鼱	鼻刀劓	鼻干鼾	 
                    鼻隶齂	齊刀劑	齊艸薺	齊雨霽	齒匕齔	齒斤齗	齒艮齦	齒足齪	龍宀寵	龍竹籠	 
                    龍艸蘢	龜鬥鬮	龠竹籥	龠艸蘥'''

    threeRadTrees = '''一冖士殳𣪊 		𣪥	㲄	㝅	彀	榖	穀	縠	觳	𣫂	鷇	 
一田聿畫 		劃	繣	 
丨二人乍 		作	筰	厏	咋	岞	怍	怎	拃	昨	柞	炸	痄	砟	祚	窄	搾	醡	笮	胙	葄	舴	苲	蚱	詐	迮	酢	阼	鮓	齚	 
丶巛丶丶州 		洲	詶	酬	 
丿丿勹勿 		昜	偒	傷	慯	殤	觴	鬺	場	揚	暘	楊	湯	燙	璗	盪	簜	蕩	鐋	煬	暢	痬	碭	禓	腸	逿	鍚	陽	颺	餳	匆	怱	葱	刎	吻	𠯳	脗	忽	唿	惚	昒	易	剔	埸	惕	㻛	痬	緆	裼	賜	儩	䞶	踢	錫	鬄	沕	物	笏	芴	 
丿乙丶之 		乏	泛	眨	砭	窆	覂	貶	芝	 
丿乙冖冘 		妉	忱	枕	沈	眈	紞	耽	酖	醓	髧	鴆	黕	 
丿乙口𠮠 		別	捌	莂	 
丿勹禾𥝢 		棃	犂	鯬	黧	 
丿又乙及 		吸	岋	岌	扱	板	汲	笈	級	芨	衱	趿	鈒	靸	馺	 
丿火乙乙乙爪爲 		僞	 
乙丨丿丿𠂔 		姊	泲	秭	笫	胏	 
乙乙乙乙二亞 		啞	埡	堊	壺	壼	婭	惡	掗	椏	氬	瘂	稏	蝁	錏	 
亅丶人以 		似	姒	 
亅丶彐卩即 		節	 
亅丶彐无丨既 		慨	概	穊	響	鱀	 
亅丿卩卬 		仰	抑	昂	枊	迎	 
二刀邑那 		哪	挪	 
人丨攴攸 		修	悠	條	滌	篠	蓧	鰷	浟	倐	倏	絛	翛	脩	滫	蓨	莜	鯈	儵	 
人夂丶亠夜 		掖	液	腋	 
人矢一乙侯 		候	𠋫	喉	堠	猴	瘊	睺	緱	鍭	餱	 
八乙目匕眞 		塡	愼	鎭	顚	巓	 
八巾八㡀 		敝	嫳	幣	弊	彆	憋	撇	瞥	蔽	襒	蹩	鐅	鱉	鼈	虌	 
冂一冂一𠀙 		丽	麗	儷	孋	攦	曬	欐	灑	纚	躧	釃	驪	鱺	鸝	 
冂冂一册 		删	姗	栅	㹪	 
冂冂乙冎 		咼	剮	喎	渦	猧	禍	窩	緺	腡	蝸	過	撾	檛	濄	薖	鍋	 
冂大丿𡗠 		𪥌	𡘠	奥	奧	噢	墺	懊	澳	燠	薁	襖	袄	鐭	隩	 
冖臼爻𦥯 		學	斅	斆	嶨	澩	礐	覺	攪	鱟	鷽	黌	 
冫儿丶丿兆 		佻	垗	姚	庣	恌	挑	晁	朓	桃	洮	狣	珧	眺	祧	䄻	窕	筄	覜	誂	跳	逃	銚	頫	駣	鮡	鼗	 
匚一虍虐 		㖸	瘧	謔	 
厂小白原 		塬	愿	源	縓	羱	螈	豲	願	騵	 
厂彡文彥 		喭	諺	顏	 
厂生文產 		剷	㯆	滻	鏟	隡	薩	 
又冖彐𠬶 		侵	唚	梫	浸	祲	綅	鋟	 
又网日曼 		僈	墁	嫚	幔	慢	漫	獌	縵	蔓	謾	鏝	鬘	鰻	 
口艸羊善 		墡	繕	膳	鱔	 
囗夕丶囱 		悤	傯	總	聰	蔥	驄	窗	 
夂儿田畟 		稷	謖	 
夊日人复 		復	履	蕧	覆	愎	腹	蝮	複	輹	馥	鰒	 
大乙口吳 		俁	娛	虞	澞	誤	麌	 
大幺爪奚 		傒	徯	溪	蒵	螇	謑	谿	貕	蹊	雞	騱	鷄	鼷	 
女聿亠妻 		凄	悽	棲	淒	緀	萋	 
子冖十孛 		勃	渤	葧	悖	浡	脖	餑	 
子口亠享 		孰	塾	熟	嚲	啍	埻	惇	敦	墩	憝	撴	暾	燉	礅	譈	蹾	鐓	椁	淳	焞	䇏	諄	郭	廓	槨	霩	鞹	醇	錞	鶉	𪏆	 
小乙目県 		縣	懸	纛	 
小口亠京 		倞	凉	剠	勍	就	僦	蹴	鷲	弶	掠	景	影	憬	璟	顥	灝	晾	椋	涼	諒	輬	鯨	黥	麖	 
尸口乙局 		侷	挶	梮	跼	鋦	 
尸示寸尉 		慰	熨	罻	蔚	螱	𧕈	褽	霨	 
屮勹屮勹芻 		㑳	㥮	搊	皺	篘	縐	蒭	謅	趨	雛	騶	齺	 
工巛一巠 		俓	剄	勁	葝	巰	娙	徑	氫	涇	烴	牼	痙	硜	經	羥	脛	莖	輕	鑋	逕	陘	頸	鵛	 
巾冖彐帚 		婦	歸	𨺔	 
幺隹亠雍 		噰	壅	擁	甕	罋	臃	饔	 
广彐人庚 		賡	 
广用聿庸 		傭	墉	慵	鏞	鱅	 
廾犬艸莽 		漭	蟒	 
弓丿丨弗 		佛	刜	咈	怫	拂	氟	沸	狒	疿	笰	紼	茀	費	鐨	髴	 
彐工爪𤔌 		㥯	穩	䌥	隱	癮	讔	 
彡小白㣎 		穆	 
心乙网十㥁 		德	 
方穴自臱 		櫋	邊	籩	 
无无曰朁 		僭	噆	憯	潛	熸	簪	譖	鐕	 
日田八曾 		朆	僧	噌	增	層	嶒	憎	橧	甑	矰	磳	繒	罾	贈	蹭	驓	鬙	䰝	 
止弋一武 		虣	斌	贇	賦	 
水一丶求 		㐜	俅	救	梂	毬	球	絿	脙	裘	觩	賕	逑	銶	 
火勹臼舄 		冩	寫	瀉	潟	磶	 
片一爿𣶒 		淵	奫	肅	嘯	簫	繡	蕭	鏽	驌	 
牛冖玄牽 		縴	 
用十丶甫 		匍	哺	圃	尃	傅	博	簙	搏	溥	簿	薄	縛	膊	賻	鎛	髆	䶈	捕	晡	浦	蒲	𤗃	牖	痡	盙	簠	脯	補	輔	逋	酺	鋪	餔	黼	 
疋田冖十疐 		嚏	懥	 
皿八艸益 		蠲	嗌	搤	溢	縊	膉	艗	螠	謚	鎰	隘	鷁	齸	 
示士欠款 		窾	 
糸冖十索 		嗦	𧎳	 
网网网𦋹 		奰	 
羊羊羊羴 		羼	 
耳攴丨一敢 		𠪚	嚴	儼	巖	釅	厳	噉	憨	澉	瞰	闞	矙	 
肉人水脊 		瘠	蹐	 
舛冖爪舜 		僢	瞬	蕣	 
艸丨丨业 		亚	並	掽	普	碰	譜	鐠	虚	嘘	虛	噓	墟	歔	覷	對	懟	轛	 
豆冖士壹 		亄	懿	噎	曀	殪	豷	饐	鷧	 
豕一冖冡 		蒙	幪	懞	𣋡	朦	濛	矇	蠓	饛	鸏'''

    twoRadRoots = twoRadRoots.split()
    twoRadTrees = twoRadTrees.split('\n')
    twoRadStumps = twoRadStumps.split()
    threeRadTrees = [line.split(' 		') for line in threeRadTrees.split('\n')]
    
    return render_template('about.html', 
                            twoRadRoots=twoRadRoots,
                            twoRadTrees=twoRadTrees,
                            twoRadStumps=twoRadStumps,
                            threeRadTrees=threeRadTrees)


@functions.route('/list/<what>/<value>')
@functions.route('/list/<what>/<value>/<wholeWord>')
def getList(what, value=None, wholeWord=None):

    value = urllib.parse.unquote(value)

    if value == 'null':
        return jsonify({'items': []})

    listArray = []

    if what.startswith('chooseMeaning'):
        meanings = db.session.query(kangxi).filter_by(id=value).with_entities('english', 'russian').first()
        value = meanings[0].split(';') + meanings[1].split(';')

    elif what.startswith('chooseSynChar'):
        # query = sa.text(f"SELECT id, kangxi FROM kangxi WHERE english LIKE '%;{value};%' OR russian LIKE '%;{value};%' OR LEFT(TRIM(BOTH FROM english), {len(value)+1}) = '{value};' OR LEFT(TRIM(BOTH FROM russian), {len(value)+1}) = '{value};' OR RIGHT(TRIM(BOTH FROM english), {len(value)+1}) = ';{value}' OR RIGHT(TRIM(BOTH FROM russian), {len(value)+1}) = ';{value}' OR TRIM(BOTH FROM english) = '{value}' OR TRIM(BOTH FROM russian) = '{value}'")

        query = sa.text(f"SELECT id, kangxi FROM kangxi WHERE english LIKE '%;{value};%' OR russian LIKE '%;{value};%' OR SUBSTR(TRIM(english), 1, {len(value)+1}) = '{value};' OR SUBSTR(TRIM(russian), 1, {len(value)+1}) = '{value};' OR SUBSTR(TRIM(english), -{len(value)+1}, {len(value)+1}) = ';{value}' OR SUBSTR(TRIM(russian), -({len(value)+1}), {len(value)+1}) = ';{value}' OR TRIM(english) = '{value}' OR TRIM(russian) = '{value}'")
        value = list(db.engine.execute(query))

    elif what.startswith('treeTrunk') or what.startswith('branchRoots'):
        root = db.session.query(kangxi).filter_by(id=value).with_entities('root').first()[0]
        if what.startswith('treeTrunk'):
            value = db.session.query(kangxi).filter_by(root=root).filter_by(derivedFrom=0).with_entities('id', 'kangxi').all()
        elif what.startswith('branchRoots'):
            value = db.session.query(kangxi).filter_by(root=root).filter_by(branchRoot=1).with_entities('id', 'kangxi').all()

    elif what.startswith('branchCharacters'):
        valueChar = db.session.query(kangxi).filter_by(id=value).with_entities('kangxi').first()[0]
        query = sa.text(f"SELECT id, kangxi FROM kangxi WHERE derivedFrom LIKE '%{valueChar}%'")
        value = list(db.engine.execute(query))

    elif what == 'chooseCharacter2':
        radicals = Counter(value)
        queryLike = ' AND '.join([f"LENGTH(structure) - LENGTH(REPLACE(structure, '{radical}', '')) >= {radicals[radical]}" for radical in radicals.keys()])
        # query = sa.text(f"SELECT id, kangxi FROM kangxi WHERE {queryLike} AND CHAR_LENGTH(structure) >= {len(value)}")
        query = sa.text(f"SELECT id, kangxi FROM kangxi WHERE {queryLike}")

        value = list(db.engine.execute(query))

    elif what == 'rootList3':
        radicals = Counter(value)
        queryLike = ' AND '.join([f"LENGTH(structure) - LENGTH(REPLACE(structure, '{radical}', '')) >= {radicals[radical]}" for radical in radicals.keys()])
        # query = sa.text(f"SELECT id, kangxi FROM kangxi WHERE {queryLike} AND CHAR_LENGTH(structure) >= {len(value)} AND (branchRoot = 1 OR structure = root)")
        query = sa.text(f"SELECT id, kangxi FROM kangxi WHERE {queryLike} AND (branchRoot = 1 OR treeRoot = 1)")
        value = list(db.engine.execute(query))

    elif what == 'tree3':
        rootQuery = db.session.query(kangxi).filter_by(id=value).with_entities('kangxi', 'treeRoot', 'branchRoot', 'root').first()
        #Branch roots
        if rootQuery[2] == '1':
            queryLike = f"derivedFrom LIKE '%{rootQuery[0]}%'"
            query = sa.text(f"SELECT id, kangxi FROM kangxi WHERE {queryLike}")
            value = list(db.engine.execute(query))
        #Tree roots
        elif rootQuery[1] == '1':
            value = db.session.query(kangxi).filter_by(root=rootQuery[3]).with_entities('id', 'kangxi').all()
            #Exclude the tree root itself
            value = value[1:]

    elif what == 'allMeanings4':
        if wholeWord == 'n':
            # query = sa.text(f"SELECT meaning, meaning FROM meanings WHERE meaning = '{value}' OR meaning LIKE '% {value} %' OR LEFT(TRIM(BOTH FROM meaning), {len(value)+1}) = '{value} ' OR RIGHT(TRIM(BOTH FROM meaning), {len(value)+1}) = ' {value}'")
            query = sa.text(f"SELECT meaning, meaning FROM meanings WHERE meaning = '{value}' OR meaning LIKE '% {value} %' OR SUBSTR(TRIM(meaning), 1, {len(value)+1}) = '{value} ' OR SUBSTR(TRIM(meaning), -{len(value)+1}, {len(value)+1}) = ' {value}'")
        elif wholeWord == 'y':
            query = sa.text(f"SELECT meaning, meaning FROM meanings WHERE meaning LIKE '%{value}%'")
        value = list(db.engine.execute(query))

    if what.startswith('chooseStructureElement') and not what.endswith('3'):
        value = value[:-1]

    for char in value:

        charObj = {}
        if what == 'chooseCharacter' or what.startswith('chooseStructureElement'):
            try:
                characterInDB = db.session.query(kangxi).filter_by(kangxi=char).with_entities('id').first()[0]
            except:
                continue
            charObj['id'] = characterInDB 
            charObj['item'] = char
        elif what.startswith('chooseMeaning'):
            if char == '':
                continue
            charObj['id'] = char
            charObj['item'] = char
        else:
            charObj['id'] = char[0]
            charObj['item'] = char[1]
        listArray.append(charObj)

    return jsonify({'items': listArray})


@functions.route('/value/<what>/<characterID>')
def getValue(what, characterID):

    characterID = urllib.parse.unquote(characterID)

    if characterID == 'null':
        return jsonify({'items': []})

    if what.startswith('structure'):
        value = db.session.query(kangxi).filter_by(id=characterID).with_entities('structure').first()[0]

    elif 'Meanings' in what:
        if what.startswith('rootMeanings'):
            meaning = db.session.query(kangxi).filter_by(kangxi=characterID).with_entities('english', 'russian').first()
        else:
            meaning = db.session.query(kangxi).filter_by(id=characterID).with_entities('english', 'russian').first()
        value = [mean for mean in meaning[0].split(';') + meaning[1].split(';') if mean != '']
        value = ', '.join(value)
        
    return jsonify({'items': value})
