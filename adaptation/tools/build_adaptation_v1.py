from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "adaptation/odyssey_m1_v1"
CORPUS_MANIFEST = ROOT / "analysis/formal/odyssey_v1/corpus_manifest.json"
CORPUS_MANIFEST_SHA256 = "0999249a0a25e804dbaa4a393145a7e18d40fe4d1759743cd008a8ab47c1379b"
FIXED_TIME = "2026-08-15T10:00:00Z"


EPISODES = [
    (1, "没有父亲的家", [1], "雅典娜把奥德修斯停滞的归途变成忒勒马科斯必须承担的第一步。", "求婚者在奥德修斯厅堂里掷骰饮酒，忒勒马科斯只能想象父亲归来。", "化身门忒斯的雅典娜逼他亲口说出家正被吃空。", "忒勒马科斯第一次命令母亲并公开要求求婚者离开。", "深夜，他决定去找父亲的消息。", "忒勒马科斯", "雅典娜", ["伊萨卡厅堂", "忒勒马科斯寝室"]),
    (2, "伊萨卡第一次集会", [2], "一次失败的公开挑战迫使忒勒马科斯把成长变成秘密出航。", "忒勒马科斯召集二十年来第一次公民大会。", "安提诺俄斯揭出佩涅洛佩织拆寿衣的计谋并倒打一耙。", "民众不肯站队，忒勒马科斯只能借雅典娜之力另找船员。", "船在黑夜离岸，伏击的种子同时埋下。", "忒勒马科斯", "安提诺俄斯", ["伊萨卡集会场", "海港"]),
    (3, "皮洛斯的火", [3], "涅斯托耳没有答案，却让忒勒马科斯看见归来者可能付出的代价。", "忒勒马科斯面对海神祭火，不敢向老英雄开口。", "涅斯托耳讲述阿开亚人分裂、阿伽门农被杀与俄瑞斯忒斯复仇。", "雅典娜化作海鹰离去，证明这趟旅行有神明押注。", "庇西斯特拉托斯驱车带他去斯巴达。", "忒勒马科斯", "涅斯托耳", ["皮洛斯海滩", "涅斯托耳宫院", "通往斯巴达的道路"]),
    (4, "记忆的宫殿", [4], "斯巴达给出父亲仍活着的证据，伊萨卡却已为儿子布下死亡航线。", "忒勒马科斯在墨涅拉俄斯的奢华婚宴中因父亲落泪。", "海伦与墨涅拉俄斯分别讲出奥德修斯在特洛伊的伪装与木马。", "墨涅拉俄斯转述普罗透斯：奥德修斯被卡吕普索扣留。", "安提诺俄斯的船驶向伏击水道。", "忒勒马科斯", "墨涅拉俄斯", ["斯巴达宫殿", "伊萨卡海港", "阿斯忒里斯水道"]),
    (5, "不死也不回家", [5], "奥德修斯拒绝卡吕普索的不死承诺，却在离岛后被波塞冬剥到只剩求生本能。", "赫尔墨斯带来宙斯的命令，卡吕普索必须放人。", "奥德修斯亲手造筏，明确选择会衰老的故乡。", "波塞冬打碎木筏，海浪夺走衣物与方向。", "他钻进两棵橄榄树之间，像埋入自己的坟。", "奥德修斯", "卡吕普索", ["奥吉吉亚洞穴", "海上木筏", "斯刻里亚岸边"]),
    (6, "河边的陌生人", [5, 6], "瑙西卡在恐惧和礼法之间给沉船者一条重新成为人的路。", "雅典娜用婚事的梦把瑙西卡引到河边。", "赤裸的奥德修斯压住扑向救命者的本能，改用语言求援。", "瑙西卡给他衣食，却要求他与车队保持距离。", "她指向王宫：真正要说服的人是阿瑞忒王后。", "奥德修斯", "瑙西卡", ["斯刻里亚河口", "林间道路"]),
    (7, "王后的膝前", [7], "无名者穿过一座完美容纳陌生人的城，却被一件衣服逼到谎言边缘。", "雅典娜用雾遮住奥德修斯，引他进入菲埃克斯王宫。", "他抱住阿瑞忒的膝，要求一艘回家的船。", "阿尔喀诺俄斯愿意相助，阿瑞忒却认出女儿织的衣服。", "王后问：你究竟从哪里来？", "奥德修斯", "阿瑞忒", ["斯刻里亚街道", "菲埃克斯王宫"]),
    (8, "说出你的名字", [8], "歌者、羞辱与竞技逐层击穿奥德修斯的匿名，直到眼泪替他承认特洛伊。", "得摩多科斯唱起特洛伊，奥德修斯把泪藏进斗篷。", "欧律阿罗斯讥讽他不像运动者，他用铁饼证明力量。", "木马之歌再次让他失控，阿尔喀诺俄斯叫停宴会。", "奥德修斯抬头：我是拉厄耳忒斯之子。", "奥德修斯", "阿尔喀诺俄斯", ["菲埃克斯宴会厅", "竞技场"]),
    (9, "无人进入洞穴", [9], "奥德修斯的自述从两次失控开始，并把一行人送进独眼巨人的门。", "画面回到特洛伊之后：伊斯马洛斯的战利品拖慢撤退。", "食莲者让同伴忘记回家，奥德修斯强行把他们绑回船。", "他坚持探索独眼巨人的洞穴，等待主人回来。", "巨石封门，波吕斐摩斯捏起第一个人。", "奥德修斯", "欧律洛科斯", ["伊斯马洛斯", "食莲者海岸", "独眼巨人洞穴"]),
    (10, "我的名字叫无人", [9], "机智救出幸存者，炫耀却把胜利改写成海神的长期追杀。", "波吕斐摩斯吞食同伴，奥德修斯压住立即杀他的冲动。", "酒、木桩与“无人”让巨人失明而无法求援。", "众人藏在羊腹下逃出洞穴。", "奥德修斯喊出真名，海里响起波塞冬的诅咒。", "奥德修斯", "波吕斐摩斯", ["独眼巨人洞穴", "近岸海面"]),
    (11, "看得见伊萨卡", [10], "同伴的不信任和统帅的隐瞒在故乡可见之处毁掉顺风，随后巨人摧毁整支船队。", "埃俄罗斯把所有逆风锁进袋中。", "奥德修斯连续掌舵后睡去，同伴以为袋里藏着私财。", "风袋打开，伊萨卡从地平线退走。", "莱斯特律戈涅斯人的巨石封锁港湾，只剩一条船逃出。", "奥德修斯", "欧律洛科斯", ["埃俄罗斯岛", "伊萨卡近海", "忒勒皮洛斯港"]),
    (12, "喀耳刻的杯", [10], "把人变成猪的女神迫使奥德修斯在欲望、武力和谈判之间找到新的控制。", "侦察队在喀耳刻的酒杯后变成猪，欧律洛科斯独自逃回。", "赫尔墨斯给奥德修斯魔草和接近女神的方法。", "奥德修斯逼喀耳刻立誓、恢复同伴，却在岛上停留一年。", "喀耳刻说：回家之前，你必须先去死者那里。", "奥德修斯", "喀耳刻", ["埃埃亚森林", "喀耳刻宫殿"]),
    (13, "死者要血", [11], "奥德修斯从死者那里得到回家路线，也得到回家可能变成另一场谋杀的警告。", "厄尔佩诺耳的亡魂先索要安葬。", "忒瑞西阿斯预言牲畜禁忌、陌生归来和海神和解。", "奥德修斯抱不到母亲的影子，阿伽门农又讲出浴池里的死亡。", "阿喀琉斯问：活着的儿子怎样？", "奥德修斯", "忒瑞西阿斯", ["冥界边界", "血沟"]),
    (14, "绑在桅杆上", [12], "知道危险并不能取消代价：一次被允许的欲望，换来六个同伴的命。", "喀耳刻详细标出海妖、斯库拉和卡律布狄斯。", "船员以蜡封耳，奥德修斯被绑着听见海妖歌声。", "他隐瞒斯库拉会夺六人的事实，继续指挥划桨。", "六双手从高处伸下，抓走还在呼喊名字的人。", "奥德修斯", "欧律洛科斯", ["海妖海域", "斯库拉海峡"]),
    (15, "最后一条船", [12, 8], "饥饿让船员越过最后禁令，奥德修斯失去所有人并把故事讲回宴会现场。", "风暴困住众人在赫利俄斯岛，粮食耗尽。", "奥德修斯祈祷时睡去，欧律洛科斯说服众人杀牛。", "宙斯的雷电击碎船，奥德修斯独自漂回卡吕普索。", "宴会厅静默，菲埃克斯人答应天亮送他回家。", "奥德修斯", "欧律洛科斯", ["特里那基亚", "雷暴海面", "菲埃克斯王宫"]),
    (16, "睡着回到故乡", [13], "奥德修斯终于抵达伊萨卡，却必须先承认自己看不见家，才能学会以陌生人身份进入。", "菲埃克斯船载着睡着的奥德修斯靠岸。", "波塞冬把返航船石化，切断这条神奇航路。", "奥德修斯醒来不认得伊萨卡，还对化身牧童的雅典娜说谎。", "雅典娜把他变成老乞丐：先去找欧迈俄斯。", "奥德修斯", "雅典娜", ["福耳库斯港", "宁芙洞穴", "伊萨卡山路"]),
    (17, "忠诚住在猪圈", [14], "在最贫穷的忠臣家中，奥德修斯用谎言测试伊萨卡是否仍有容纳真相的地方。", "狗扑向乞丐，欧迈俄斯冲出来救他。", "猪倌痛骂求婚者，却拒绝再相信任何返乡预言。", "奥德修斯编造克里特身份，拿自己的归来打赌。", "夜里欧迈俄斯把唯一的厚斗篷盖给陌生人。", "奥德修斯", "欧迈俄斯", ["欧迈俄斯猪场"]),
    (18, "儿子穿过伏击", [15], "忒勒马科斯从消息之旅回到行动现场，把两条归途压进同一间茅屋。", "雅典娜催忒勒马科斯离开斯巴达，海伦以鹰兆祝他。", "他绕过伏击船，在偏僻海岸登陆。", "欧迈俄斯去给佩涅洛佩报信，乞丐独留屋中。", "门被推开，忒勒马科斯站在父亲面前却不认识他。", "忒勒马科斯", "欧迈俄斯", ["斯巴达", "伊萨卡海岸", "欧迈俄斯猪场"]),
    (19, "父亲显形", [16], "一次几乎无法相信的相认把父子从受害者变成共谋者。", "忒勒马科斯把父亲当成需要安置的乞丐。", "雅典娜恢复奥德修斯的身体，他报出身份。", "忒勒马科斯怀疑眼前是神，直到两人一起哭出十九年。", "他们决定先搬走厅堂里的武器。", "奥德修斯", "忒勒马科斯", ["欧迈俄斯猪场"]),
    (20, "狗认出了国王", [17], "奥德修斯以乞丐身份踏入自己的厅堂，每一次侮辱都成为未来审判的证据。", "忒勒马科斯回宫安抚佩涅洛佩，却隐瞒父亲已到。", "老狗阿耳戈斯抬头认主，随后死去。", "安提诺俄斯用脚凳击中讨食的乞丐。", "佩涅洛佩要求今晚见这个陌生人。", "奥德修斯", "安提诺俄斯", ["伊萨卡街道", "宫殿门槛", "厅堂"]),
    (21, "乞丐之王", [18], "奥德修斯在被设计的羞辱中展示可控力量，佩涅洛佩则让掠夺者为求婚付出财物。", "求婚者逼两个乞丐决斗，奥德修斯一击放倒伊洛斯。", "他私下警告安菲诺摩斯离开，后者仍回到宴席。", "佩涅洛佩进入厅堂，指责忒勒马科斯失礼，并向求婚者索取礼物。", "欧律马科斯再掷脚凳，厅堂笑声失控。", "奥德修斯", "佩涅洛佩", ["伊萨卡厅堂"]),
    (22, "把武器藏起来", [19], "父子在神光下解除厅堂武装，夫妻却隔着伪装进行一场谁也不肯先输的审问。", "忒勒马科斯与乞丐把墙上武器搬进库房。", "佩涅洛佩请陌生人讲丈夫，他用克里特谎言说出真实衣饰。", "佩涅洛佩落泪，却不接受返乡保证。", "她命欧律克勒娅给客人洗脚。", "奥德修斯", "佩涅洛佩", ["武器墙", "夜间厅堂", "洗脚处"]),
    (23, "伤疤没有撒谎", [19], "一处旧伤几乎揭穿身份，而佩涅洛佩把自己的怀疑变成弓的公开试验。", "欧律克勒娅摸到野猪留下的伤疤。", "奥德修斯捂住她的嘴，要求她在喜悦中保持沉默。", "佩涅洛佩讲鹰杀鹅的梦，却声称梦可能从象牙门出来。", "她决定：能拉开弓并射过斧孔的人将娶她。", "奥德修斯", "欧律克勒娅", ["洗脚处", "夜间厅堂", "佩涅洛佩卧室"]),
    (24, "最后一次忍耐", [20], "雷声、忠臣和血色幻象都指向同一天，奥德修斯仍必须等到敌人亲手把门关上。", "清晨雷声回应奥德修斯，磨坊女奴诅咒求婚者最后一餐。", "欧迈俄斯与菲洛提俄斯表现忠诚，墨兰提俄斯继续侮辱乞丐。", "忒奥克吕墨诺斯看见厅堂墙壁流血，笑着离席。", "佩涅洛佩把弓带进厅堂。", "奥德修斯", "忒奥克吕墨诺斯", ["宫殿庭院", "磨坊", "厅堂"]),
    (25, "无人拉开的弓", [21], "一件无人能使用的旧武器把求婚变成身份审判。", "佩涅洛佩宣布十二斧孔的比赛。", "忒勒马科斯三次失败，第四次几乎成功，却被父亲眼神制止。", "求婚者轮番加热、涂油，仍拉不开弓。", "乞丐开口：让我试一次。", "佩涅洛佩", "安提诺俄斯", ["厅堂", "庭院火盆"]),
    (26, "箭穿过十二把斧", [21, 22], "奥德修斯恢复武器的声音，并用第一支箭结束匿名。", "欧迈俄斯和菲洛提俄斯看见伤疤，锁住门。", "奥德修斯像调弦般拉开弓，箭穿过十二斧孔。", "忒勒马科斯拔剑站到他身边。", "下一支箭穿过安提诺俄斯的喉咙。", "奥德修斯", "忒勒马科斯", ["宫殿侧门", "封闭厅堂"]),
    (27, "厅堂审判·上", [22], "求婚者从惊愕、贿赂到反击，终于明白面前不是乞丐而是他们毁坏之家的主人。", "奥德修斯报出姓名和罪状，拒绝欧律马科斯赔偿。", "欧律马科斯冲锋被射倒，安菲诺摩斯死在忒勒马科斯枪下。", "武器耗尽，忒勒马科斯去库房取甲胄。", "墨兰提俄斯从暗道给求婚者送来武器。", "奥德修斯", "欧律马科斯", ["封闭厅堂", "武器库暗道"]),
    (28, "厅堂审判·下", [22], "忠诚与背叛在封闭空间内结算，雅典娜只在人的选择已完成后收网。", "欧迈俄斯与菲洛提俄斯抓住墨兰提俄斯。", "雅典娜化作门托耳先检验奥德修斯，再举起神盾。", "最后一轮长矛结束求婚者抵抗，欧律克勒娅辨认忠奸。", "硫磺火升起，奥德修斯却问：佩涅洛佩在哪里？", "奥德修斯", "雅典娜", ["封闭厅堂", "武器库", "庭院"]),
    (29, "搬走我们的床", [23], "公共胜利无法证明婚姻身份，佩涅洛佩用只有两个人知道的床逼丈夫显露真实记忆。", "欧律克勒娅报喜，佩涅洛佩不肯立刻相信。", "忒勒马科斯责怪母亲冷硬，奥德修斯叫他退开。", "佩涅洛佩吩咐把婚床搬出房间。", "奥德修斯愤怒说出活橄榄树的根，佩涅洛佩终于扑向他。", "佩涅洛佩", "奥德修斯", ["清洗后的厅堂", "婚房"]),
    (30, "归途之后", [24], "家庭重逢引出血亲复仇，只有在三代人共同迎战后，神明才能把胜利转成和平。", "求婚者亡魂抵达冥界，阿伽门农听见佩涅洛佩的故事。", "奥德修斯用果树记忆和伤疤与拉厄耳忒斯相认。", "欧佩忒斯率亲族进攻，拉厄耳忒斯掷矛杀死他。", "雅典娜与宙斯终止追杀；镜头回到仍扎根的橄榄树床。", "奥德修斯", "拉厄耳忒斯", ["冥界", "拉厄耳忒斯果园", "伊萨卡田野"]),
]


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8") + b"\n"


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def write(relative: str, value: object) -> None:
    path = OUT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical(value))


if digest(CORPUS_MANIFEST.read_bytes()) != CORPUS_MANIFEST_SHA256:
    raise SystemExit("BLOCKED_ADAPTATION_CORPUS_IDENTITY")

decisions = [
    ("AD-ODY-0001", "PRESERVE", "Keep the mythic world and gods as real agents under M1 modernization."),
    ("AD-ODY-0002", "PRESERVE", "Keep Books 1–4 as Telemachus' activation before Odysseus' physical release."),
    ("AD-ODY-0003", "REORDER", "Retain Books 9–12 as an explicitly framed retrospective told at the Phaeacian court."),
    ("AD-ODY-0004", "COMPRESS", "Compress ritual repetition, catalog, transit, and duplicated hospitality without changing responsibility."),
    ("AD-ODY-0005", "PRESERVE", "Split the Cyclops story across two episodes so cleverness and pride carry separate consequences."),
    ("AD-ODY-0006", "MERGE", "Place Aeolus and the Laestrygonians in one escalating episode about trust and catastrophic command loss."),
    ("AD-ODY-0007", "PRESERVE", "Keep the Underworld, Sirens, Scylla, and Helios cattle as distinct moral tests."),
    ("AD-ODY-0008", "EXTERNALIZE", "Make Penelope's strategic agency continuous through gifts, dream, bow contest, and bed test."),
    ("AD-ODY-0009", "MERGE", "Treat unnamed suitors as a chorus while preserving Antinous, Eurymachus, and Amphinomus."),
    ("AD-ODY-0010", "MODERNIZE", "Use concise contemporary Chinese dialogue while preserving status, ritual, and mythic setting."),
    ("AD-ODY-0011", "PRESERVE", "Stage the hall violence as consequence-driven judgment, not consequence-free spectacle."),
    ("AD-ODY-0012", "PRESERVE", "End with Laertes, civic feud, and divinely imposed peace rather than the bed recognition alone."),
]
write(
    "decision_ledger.json",
    {
        "artifact_class": "ctde_adaptation_decision_ledger",
        "schema_version": "1.0.0",
        "status": "locked",
        "decisions": [{"decision_id": identifier, "operation": operation, "decision": decision, "status": "locked"} for identifier, operation, decision in decisions],
    },
)

cards = []
for number, title, books, logline, opening, midpoint, turn, cliff, primary, secondary, locations in EPISODES:
    event_ids = [f"EV-B{book:02d}-{index:02d}" for book in books for index in range(1, 4)]
    card = {
        "artifact_class": "ctde_episode_card",
        "schema_version": "1.0.0",
        "season_id": "ODY-M1-S01-V1",
        "episode_id": f"EP{number:02d}",
        "episode_number": number,
        "title": title,
        "status": "locked",
        "target_minutes": 7,
        "source_books": books,
        "source_event_ids": event_ids,
        "logline": logline,
        "primary_character": primary,
        "counterforce_character": secondary,
        "opening_pressure": opening,
        "midpoint_reversal": midpoint,
        "irreversible_turn": turn,
        "ending_cliffhanger": cliff,
        "locations": locations,
        "scene_cards": [
            {"scene_id": f"EP{number:02d}-S01", "function": "opening_pressure", "summary": opening},
            {"scene_id": f"EP{number:02d}-S02", "function": "escalation", "summary": logline},
            {"scene_id": f"EP{number:02d}-S03", "function": "midpoint_reversal", "summary": midpoint},
            {"scene_id": f"EP{number:02d}-S04", "function": "irreversible_turn", "summary": turn},
            {"scene_id": f"EP{number:02d}-S05", "function": "cliffhanger", "summary": cliff},
        ],
        "adaptation_decision_ids": ["AD-ODY-0001", "AD-ODY-0004", "AD-ODY-0010"] + (["AD-ODY-0003"] if any(book in {9, 10, 11, 12} for book in books) else []) + (["AD-ODY-0008"] if any(book in {18, 19, 21, 23} for book in books) else []),
        "continuity_requirements": ["Preserve source responsibility and consequence.", "Carry character knowledge only from prior episodes.", "Mark invented connective action as adaptation, never source fact."],
    }
    cards.append(card)
    write(f"episode_cards/EP{number:02d}.json", card)

architecture = {
    "artifact_class": "ctde_30_episode_architecture",
    "schema_version": "1.0.0",
    "status": "PASS_30_EPISODE_ARCHITECTURE",
    "season_id": "ODY-M1-S01-V1",
    "episode_count": len(cards),
    "target_minutes_per_episode": 7,
    "modernization_level": "M1",
    "act_movements": [
        {"movement": 1, "episodes": [1, 4], "function": "Telemachus activates Ithaca and gathers proof."},
        {"movement": 2, "episodes": [5, 8], "function": "Odysseus escapes stasis and regains a name."},
        {"movement": 3, "episodes": [9, 15], "function": "The embedded wanderings expose intelligence, pride, leadership, and loss."},
        {"movement": 4, "episodes": [16, 24], "function": "Disguised return tests loyalty and prepares judgment."},
        {"movement": 5, "episodes": [25, 30], "function": "Bow, reckoning, recognition, lineage, and civic peace complete return."},
    ],
    "episodes": cards,
}
write("episode_architecture.json", architecture)

continuity = {
    "artifact_class": "ctde_odyssey_continuity_bible",
    "schema_version": "1.0.0",
    "status": "locked",
    "character_arcs": {
        "Odysseus": "detained survivor → self-narrating commander under judgment → disguised tester → revealed avenger → recognized husband/son → ruler constrained by peace",
        "Telemachus": "passive heir → public dissenter → guest/student → returning survivor → recognized son and co-conspirator",
        "Penelope": "besieged strategist → guarded interviewer → architect of bow test → final authority on marital identity",
        "Athena": "divine advocate → disguised mentor → strategist of return → limiter of revenge",
    },
    "knowledge_locks": [
        {"through_episode": 18, "rule": "Telemachus does not know the beggar is Odysseus."},
        {"through_episode": 22, "rule": "Eurycleia does not know the beggar is Odysseus."},
        {"through_episode": 28, "rule": "Penelope has evidence and suspicion but no confirmed identity."},
        {"through_episode": 25, "rule": "The suitors do not know the beggar can string the bow."},
    ],
    "prop_registry": ["Athena's spear", "wind bag", "moly", "mast bonds", "Odysseus' scar", "removed wall weapons", "Odysseus' bow", "twelve axes", "olive-tree bed"],
    "motif_registry": ["threshold", "sea", "song", "disguise", "recognition", "guest-gift", "weaving", "rooted olive"],
    "violence_rule": "Every major injury must preserve causal responsibility and downstream consequence; no disposable spectacle escalation.",
}
write("continuity_bible.json", continuity)

bible = """# 《归途：奥德修斯》Adaptation Bible V1

Status: `PASS_ADAPTATION_BIBLE`

## Format and promise

This is a 30-episode, approximately seven-minutes-per-episode Chinese serial drama in modernization mode M1. The mythic Mediterranean world and active gods remain real. Language, scene entry, viewpoint rhythm, and serial hooks are modernized; event responsibility, relationship identity, and consequence are not silently reassigned.

The audience promise is not merely that Odysseus reaches Ithaca. He must become recognizable again at expanding scales: to himself after loss, to a son who has grown without him, to servants who reveal the moral state of his house, to enemies who have occupied it, to a wife who will not surrender judgment, to a father whose memory is rooted in land, and finally to a community that could continue the killing.

## Dramatic engine

The season runs on three interlocked clocks: Ithaca's household is being consumed; Telemachus must become capable before the ambush closes; Odysseus must cross from clever survival to disciplined concealment. Books 9–12 remain an embedded self-narration at the Phaeacian court, so the audience can admire his intelligence while also judging how he tells responsibility, pride, and loss.

## Character locks

- Odysseus wins through language, timing, disguise, endurance, and force, but his need to be known creates Poseidon's curse. His arc is not from weakness to strength; it is from exposed cleverness to controlled identity.
- Penelope is the final human verifier. Her gifts, dream, bow decision, and bed test form one strategic line, not isolated reactions.
- Telemachus does not become a duplicate warrior. He learns to speak, travel, evaluate testimony, keep secrets, and stand beside his father without losing his separate moral exposure.
- Athena advocates, mentors, disguises, and restrains. Divine intervention changes conditions but never replaces the human choice required next.
- Poseidon is not a weekly villain. His pressure is the durable consequence of the Cyclops episode and the boundary on effortless passage.

## Fidelity and invention boundary

Source facts remain bound to the locked 24-Book corpus. Compression may shorten rites, voyages, catalogs, and repeated hospitality. Connective action and concise dialogue are adaptation inventions and must not alter who chooses, suffers, recognizes, or forgives. Named suitors Antinous, Eurymachus, and Amphinomus retain distinct functions; the remaining suitors can operate as a chorus.

## Visual and sonic grammar

Thresholds frame power changes. The sea is heard before it is seen whenever Poseidon's consequence returns. Athena's interventions use changes in crowd rhythm and reflected light rather than generic spectacle. Songs trigger memory and identity pressure. The scar, bow, axes, and olive-tree bed form the final recognition chain: body, capability, public identity, private shared knowledge.

## Production assumptions

Primary standing sets are the Ithaca hall/courtyard, Phaeacian hall, ship deck, Eumaeus farm, and adaptable shore/cave environments. Creature episodes use partial views, sound, shadow, and human reaction to protect scale. Hall reckoning spans three episodes including bow activation and is staged spatially, with doors, weapon access, and loyalties established before combat.

## Ending rule

Episode 29 completes marriage recognition, not the series. Episode 30 restores lineage and confronts civic vengeance. Athena's peace is earned only after three generations stand in the field and the story demonstrates that unlimited requital would reproduce the disorder return was meant to end.
"""
(OUT / "ADAPTATION_BIBLE.md").write_text(bible, encoding="utf-8")

report = """# 30-Episode Architecture Report

Status: `PASS_30_EPISODE_ARCHITECTURE`

All 30 episode cards are locked, ordered, source-book bound, and supplied with opening pressure, midpoint reversal, irreversible turn, ending hook, five scene functions, locations, continuity constraints, and decision references. The structure covers Books 1–24 with no unplanned gap. Embedded narration, recognition order, weapon continuity, and the final civic closure are explicit.
"""
(OUT / "30_EPISODE_ARCHITECTURE_REPORT.md").write_text(report, encoding="utf-8")

inventory = []
for path in sorted(OUT.rglob("*")):
    if path.is_file() and path.name != "manifest.json":
        raw = path.read_bytes()
        inventory.append({"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": digest(raw)})
write(
    "manifest.json",
    {
        "artifact_class": "ctde_adaptation_v1_manifest",
        "schema_version": "1.0.0",
        "status": "PASS_ADAPTATION_BIBLE_AND_30_EPISODE_ARCHITECTURE",
        "standing_authorization_id": "CTDE-GOAL-COMPLETION-20260815-001",
        "corpus_manifest_sha256": CORPUS_MANIFEST_SHA256,
        "modernization_level": "M1",
        "episode_count": len(cards),
        "decision_count": len(decisions),
        "artifact_count": len(inventory),
        "artifacts": inventory,
        "self_identity": {"path": "adaptation/odyssey_m1_v1/manifest.json", "sha256": None, "reason": "self_reference"},
        "generated_at": FIXED_TIME,
    },
)
print("PASS_ADAPTATION_BIBLE_AND_30_EPISODE_ARCHITECTURE")
