# -*- coding: utf-8 -*-

import csv
import json
import os
import re
from unicodedata import combining, normalize

import arrow
import emoji
import requests
from PIL import Image, ImageDraw, ImageFont
from yaml import dump

from constant import (
    BANGUMIRANKIMG,
    C_000000,
    C_6D4B2B,
    C_818181,
    C_AC8164,
    C_BCA798,
    C_CC0000,
    C_EAAA7D,
    C_FFFFFF,
    COMBINING_CYRILLIC,
    CONTROL,
    CUNEIFORM,
    DINGBATS,
    DOWNIMG,
    DRAWIMG,
    EMOJIONE,
    FZY4K_GBK1_0,
    GOTHICA1,
    HANNOTATESC_W5,
    HISTORYRANKIMG,
    HISTORYRECORDIMG,
    HUAWENYUANTI_BOLD,
    HYM2GJ,
    LONGIMG,
    LONGTIMEIMG,
    MAINRANKIMG,
    MAINTITLEIMG,
    MATHEMATICAL_ALPHANUMERIC_SYMBOLS,
    MODIFIER_LETTER,
    SCRIPT_SIGN_SQUARE,
    SEGOE_UI,
    SEGOE_UI_HISTORIC,
    SEGOE_UI_SYMBOL,
    STATONEIMG,
    STATTHREEIMG,
    STATTWOIMG,
    STYUANTI_SC_BOLD,
    SUBBANGUMIRANKIMG,
    SUBRANKIMG,
    TOPIMG,
    UPIMG,
    WEEKS,
)

MRank = json.load(open(f"{WEEKS}_results.json", "r", encoding="utf-8"))
BRank = json.load(open(f"{WEEKS}_results_bangumi.json", "r", encoding="utf-8"))
GRank = json.load(open(f"{WEEKS}_guoman_bangumi.json", "r", encoding="utf-8"))
HRank = json.load(open(f"{WEEKS}_results_history.json", "r", encoding="utf-8"))
SRank = json.load(open(f"{WEEKS}_stat.json", "r", encoding="utf-8"))
Invalid = json.load(open("LostFile.json", "r", encoding="utf-8"))
InvalidList = Invalid["name"]

MRankData = {
    x["wid"]: {
        "author": f"{x['author']}   投稿",
        "av": x["wid"],
        "bv": x["bv"],
        "cdate": arrow.get(x["cdate"]).format("YYYY-MM-DD HH:mm"),
        "changqi": x["changqi"],
        "clicks_rank": format(x["clicks_rank"], ","),
        "clicks": format(x["clicks"], ","),
        "comments_rank": format(x["comments_rank"], ","),
        "comments": format(x["comments"], ","),
        "danmu_rank": format(x["danmu_rank"], ","),
        "danmu": format(x["danmu"], ","),
        "fix_a": (x["clicks"] + 200000) / (x["clicks"] * 2),
        "fix_b": (x["stows"] * 20 + x["yb"] * 10)
        / (x["clicks"] + x["yb"] * 10 + x["comments"] * 50),
        "fix_b_": (x["clicks"] * 50) / (x["clicks"] + x["comments"] * 50),
        "fix_c": (x["yb"] * 2000) / x["clicks"],
        "fix_p": 4 / (x["part"] + 3),
        "last": str(x["last"]),
        "part": str(x["part"]),
        "pic": x["pic"],
        "score": format(x["score"], ","),
        "score_rank": str(x["score_rank"]),
        "sp_type_id": x["sp_type_id"],
        "stows_rank": format(x["stows_rank"], ","),
        "stows": format(x["stows"], ","),
        "title": str(x["name"]),
        "weekly_id": x["weekly_id"],
        "wtype": x["wtype"],
        "yb_rank": format(x["yb_rank"], ","),
        "yb": format(x["yb"], ","),
    }
    for x in MRank
    if x.get("info") is None
}
BRankData = {
    x["wid"]: {
        "author": f"{x['author']}   投稿",
        "av": x["wid"],
        "bv": x["bv"],
        "cdate": arrow.get(x["cdate"]).format("YYYY-MM-DD HH:mm"),
        "clicks_rank": format(x["click_rank"], ","),
        "clicks": format(x["click"], ","),
        "comments_rank": format(x["comm_rank"], ","),
        "comments": format(x["comm"], ","),
        "cover": x["cover"],
        "danmu_rank": format(x["danmu_rank"], ","),
        "danmu": format(x["danmu"], ","),
        "fix_a": (x["click"] + 200000) / (x["click"] * 2),
        "fix_b": (x["stow"] * 20 + x["yb"] * 10)
        / (x["click"] + x["yb"] * 10 + x["comm"] * 50),
        "fix_b_": (x["click"] * 50) / (x["click"] + x["comm"] * 50),
        "fix_c": (x["yb"] * 2000) / x["click"],
        "fix_p": 4 / (x["part_count"] + 3),
        "last": str(x.get("last") if x.get("last") else 0),
        "part": str(x["part_count"]),
        "pic": x["pic"],
        "score": format(x["score"], ","),
        "score_rank": str(x["rank"]),
        "stows_rank": format(x["stow_rank"], ","),
        "stows": format(x["stow"], ","),
        "title": str(x["name"]),
        "weekly_id": x["weekly_id"],
        "yb_rank": format(x["yb_rank"], ","),
        "yb": format(x["yb"], ","),
    }
    for x in BRank
    if x.get("info") is None
}
GRankData = {
    x["wid"]: {
        "author": f"{x['author']}   投稿",
        "av": x["wid"],
        "bv": x["bv"],
        "cdate": arrow.get(x["cdate"]).format("YYYY-MM-DD HH:mm"),
        "clicks_rank": format(x["click_rank"], ","),
        "clicks": format(x["click"], ","),
        "comments_rank": format(x["comm_rank"], ","),
        "comments": format(x["comm"], ","),
        "cover": x["cover"],
        "danmu_rank": format(x["danmu_rank"], ","),
        "danmu": format(x["danmu"], ","),
        "fix_a": (x["click"] + 200000) / (x["click"] * 2),
        "fix_b": (x["stow"] * 20 + x["yb"] * 10)
        / (x["click"] + x["yb"] * 10 + x["comm"] * 50),
        "fix_b_": (x["click"] * 50) / (x["click"] + x["comm"] * 50),
        "fix_c": (x["yb"] * 2000) / x["click"],
        "fix_p": 4 / (x["part_count"] + 3),
        "last": str(x.get("last") if x.get("last") else 0),
        "part": str(x["part_count"]),
        "pic": x["pic"],
        "score": format(x["score"], ","),
        "score_rank": str(x["rank"]),
        "stows_rank": format(x["stow_rank"], ","),
        "stows": format(x["stow"], ","),
        "title": str(x["name"]),
        "weekly_id": x["weekly_id"],
        "yb_rank": format(x["yb_rank"], ","),
        "yb": format(x["yb"], ","),
    }
    for x in GRank
    if x.get("info") is None
}
HRankData = {
    x["wid"]: {
        "author": f"{x['author']}   投稿",
        "av": x["wid"],
        "bv": x["bv"],
        "cdate": arrow.get(x["cdate"]).format("YYYY-MM-DD HH:mm"),
        "score": format(x["score"], ","),
        "score_rank": str(x["score_rank"]),
        "title": str(x["name"]),
        "weekly_id": x["weekly_id"],
        "wtype": x["wtype"],
    }
    for x in HRank
    if x.get("info") is None
}
SRankData = {x["type"]: x.get("ranks") for x in SRank}
AllData = {
    **MRankData,
    **BRankData,
    **GRankData,
    **HRankData,
}


def Resource(bid, link, name):
    ext = link.split(".")[-1]
    if not os.path.exists(f"./pic/{bid}_{name}.{ext}"):
        resp = requests.get(link)
        with open(f"./pic/{bid}_{name}.{ext}", "wb") as f:
            f.write(resp.content)
    return f"./pic/{bid}_{name}.{ext}"


def Single(args):
    bid, rtype = args
    Author_F = ImageFont.truetype(HANNOTATESC_W5, 32)
    Bid_F = ImageFont.truetype(STYUANTI_SC_BOLD, 42)
    BiDataRank_F = ImageFont.truetype(HANNOTATESC_W5, 26)
    Cata_F = ImageFont.truetype(STYUANTI_SC_BOLD, 36)
    DataFix_F = ImageFont.truetype(STYUANTI_SC_BOLD, 32)
    Emoji_F = ImageFont.truetype(EMOJIONE, 54)
    HisRank_F = ImageFont.truetype(STYUANTI_SC_BOLD, 72)
    Invalid_F = ImageFont.truetype(FZY4K_GBK1_0, 48)
    LastRank_F = ImageFont.truetype(HANNOTATESC_W5, 36)
    Score_F = ImageFont.truetype(STYUANTI_SC_BOLD, 52)
    ScoreRank_F = ImageFont.truetype(HYM2GJ, 150)
    Title_F = ImageFont.truetype(HUAWENYUANTI_BOLD, 54)
    UnicodeA_F = ImageFont.truetype(SEGOE_UI, 54)
    UnicodeB_F = ImageFont.truetype(SEGOE_UI_SYMBOL, 54)
    UnicodeC_F = ImageFont.truetype(GOTHICA1, 54)
    UnicodeD_F = ImageFont.truetype(SEGOE_UI_HISTORIC, 54)
    Part_F = BiDataRank_F
    Data_F = UpTime_F = Cata_F
    Aid = AllData[bid]["av"]
    Author = AllData[bid]["author"]
    Bid = AllData[bid]["bv"]
    Score = AllData[bid]["score"]
    ScoreRank = AllData[bid]["score_rank"]
    Title = AllData[bid]["title"]
    UpTime = AllData[bid]["cdate"]
    Week = AllData[bid]["weekly_id"]

    ishistory = bool(str(Week) != str(WEEKS))
    RankImg = (
        Image.open(HISTORYRANKIMG)
        if ishistory
        else Image.open(MAINRANKIMG)
        if rtype
        else Image.open(BANGUMIRANKIMG)
    )
    RankPaper = ImageDraw.Draw(RankImg)

    if rtype and not ishistory and AllData[bid]["changqi"]:
        LongMark = Image.open(LONGTIMEIMG)
        LongRegion = LongMark.crop((0, 0) + LongMark.size)
        RankImg.paste(LongRegion, (11, 11))
    if not rtype:
        Cover = AllData[bid]["cover"]
        CoverFile = Resource(bid, Cover, "cover")
        IconMark = Image.open(CoverFile)
        IconRegion = IconMark.crop((0, 0) + IconMark.size)
        IconCover = IconRegion.resize((115, 115), Image.Resampling.LANCZOS)
        RankImg.paste(IconCover, (19, 929))

    ShinkSize = 0
    Title_O = 31 if rtype else 167
    NFCTitle = normalize("NFC", Title)
    NFCTitle = "".join([c for c in NFCTitle if combining(c) == 0])
    RegexTitle = re.sub(chr(65039), "", NFCTitle)
    RegexTitle = re.sub(COMBINING_CYRILLIC, "", RegexTitle)
    RegexTitle = re.sub(CONTROL, "", RegexTitle)
    while (Title_F.getlength(RegexTitle) + Title_O) > 1440:
        ShinkSize += 1
        Title_F = ImageFont.truetype(HUAWENYUANTI_BOLD, 54 - ShinkSize)
        Emoji_F = ImageFont.truetype(EMOJIONE, 54 - ShinkSize)
        UnicodeA_F = ImageFont.truetype(SEGOE_UI, 54 - ShinkSize)
        UnicodeB_F = ImageFont.truetype(SEGOE_UI_SYMBOL, 54 - ShinkSize)
        UnicodeC_F = ImageFont.truetype(GOTHICA1, 54 - ShinkSize)
        UnicodeD_F = ImageFont.truetype(SEGOE_UI_HISTORIC, 54 - ShinkSize)

    i = 0
    Title_Step = Title_O
    while i < len(RegexTitle):
        if (
            emoji.is_emoji(RegexTitle[i])
            and re.match(r"[\u2640\u2642]", RegexTitle[i]) is None
        ):
            RankPaper.text((Title_Step, 979), RegexTitle[i], C_6D4B2B, Emoji_F)
            Title_Step += Emoji_F.getlength(RegexTitle[i])
        elif re.match(CUNEIFORM, RegexTitle[i]) is not None:
            RankPaper.text(
                (Title_Step, 979),
                RegexTitle[i],
                C_6D4B2B,
                UnicodeD_F,
            )
            Title_Step += UnicodeD_F.getlength(RegexTitle[i])
        elif re.match(SCRIPT_SIGN_SQUARE, RegexTitle[i]) is not None:
            RankPaper.text(
                (Title_Step, 979),
                RegexTitle[i],
                C_6D4B2B,
                UnicodeC_F,
            )
            Title_Step += UnicodeC_F.getlength(RegexTitle[i])
        elif (
            re.match(DINGBATS, RegexTitle[i]) is not None
            or re.match(MATHEMATICAL_ALPHANUMERIC_SYMBOLS, RegexTitle[i]) is not None
        ):
            RankPaper.text(
                (Title_Step, 979 - UnicodeB_F.getbbox(RegexTitle[i])[-1] * 0.15),
                RegexTitle[i],
                C_6D4B2B,
                UnicodeB_F,
            )
            Title_Step += UnicodeB_F.getlength(RegexTitle[i])
        elif (
            (re.match(MODIFIER_LETTER, RegexTitle[i]) is not None)
            or (
                i + 1 < len(RegexTitle)
                and re.match(r"[0-9a-zA-Z\u4E00-\u9FA5]", RegexTitle[i + 1]) is None
                and re.match(MODIFIER_LETTER, RegexTitle[i + 1]) is not None
            )
            or (re.match(MODIFIER_LETTER, RegexTitle[i - 1]) is not None)
        ):
            RankPaper.text((Title_Step, 979), RegexTitle[i], C_6D4B2B, UnicodeA_F)
            Title_Step += UnicodeA_F.getlength(RegexTitle[i])
        else:
            RankPaper.text((Title_Step, 979), RegexTitle[i], C_6D4B2B, Title_F)
            Title_Step += Title_F.getlength(RegexTitle[i])
        i += 1

    Author_X = 31 if rtype else 189
    AuthorName = Author if rtype else "投稿"
    RankPaper.text((Author_X, 927), AuthorName, C_6D4B2B, Author_F)
    Bid_X = 195 - Bid_F.getlength(Bid) / 2
    RankPaper.text((Bid_X, 847), Bid, C_FFFFFF, Bid_F)

    if rtype:
        Cata = AllData[bid]["wtype"]
        Cata_X = 580 - Cata_F.getlength(Cata) / 2
        RankPaper.text((Cata_X, 849), Cata, C_6D4B2B, Cata_F)
    UpTime_O = 933 if rtype else 754
    UpTime_X = UpTime_O - UpTime_F.getlength(UpTime) / 2
    RankPaper.text((UpTime_X, 850), UpTime, C_6D4B2B, UpTime_F)
    ScoreRank_X = 1703 - ScoreRank_F.getlength(ScoreRank) / 2
    RankPaper.text((ScoreRank_X, 28), ScoreRank, C_FFFFFF, ScoreRank_F)

    Score_X = 1703 - Score_F.getlength(Score) / 2
    if ishistory:
        RankPaper.text((Score_X, 280), Score, C_FFFFFF, Score_F)
        RankPaper.text((1495, 400), f"#{Week}", C_FFFFFF, HisRank_F)
        RankImg.save(f"./ranking/list1/av{Aid}.png")
        return 0
    RankPaper.text((Score_X, 376), Score, C_FFFFFF, Score_F)

    Click = AllData[bid]["clicks"]
    ClickRank = AllData[bid]["clicks_rank"]
    Coin = AllData[bid]["yb"]
    CoinRank = AllData[bid]["yb_rank"]
    Comment = AllData[bid]["comments"]
    CommentRank = AllData[bid]["comments_rank"]
    Danmu = AllData[bid]["danmu"]
    DanmuRank = AllData[bid]["danmu_rank"]
    Stow = AllData[bid]["stows"]
    StowRank = AllData[bid]["stows_rank"]
    LastRank = AllData[bid]["last"]
    if str(LastRank) == "0":
        LastRank_X = 1703 - LastRank_F.getlength("新上榜") / 2
        RankPaper.text((LastRank_X + 2, 184 + 2), "新上榜", C_000000, LastRank_F)
        RankPaper.text((LastRank_X + 1, 184 + 1), "新上榜", C_818181, LastRank_F)
        RankPaper.text((LastRank_X, 184), "新上榜", C_FFFFFF, LastRank_F)
    else:
        LastRank_X = 1703 - LastRank_F.getlength("上周") / 2
        LastRank_X_ = 1703 + LastRank_F.getlength("上周") / 2
        RankPaper.text((LastRank_X + 2, 184 + 2), "上周", C_000000, LastRank_F)
        RankPaper.text((LastRank_X_ + 2, 184 + 2), LastRank, C_000000, LastRank_F)
        RankPaper.text((LastRank_X + 1, 184 + 1), "上周", C_818181, LastRank_F)
        RankPaper.text((LastRank_X_ + 1, 184 + 1), LastRank, C_818181, LastRank_F)
        RankPaper.text((LastRank_X, 184), "上周", C_FFFFFF, LastRank_F)
        RankPaper.text((LastRank_X_, 184), LastRank, C_FFFFFF, LastRank_F)
        if int(ScoreRank) < int(LastRank):
            StatPin = Image.open(UPIMG)
        elif int(ScoreRank) > int(LastRank):
            StatPin = Image.open(DOWNIMG)
        elif int(ScoreRank) == int(LastRank):
            StatPin = Image.open(DRAWIMG)
        PinRegion = StatPin.crop((0, 0) + StatPin.size)
        PinCover = PinRegion.resize((45, 45), Image.Resampling.BILINEAR)
        Pin_X = 1655 - int(LastRank_F.getlength("上周") / 2)
        RankImg.paste(PinCover, (Pin_X, 190), mask=PinCover)
    RankPaper.text((1535, 545), Click, C_FFFFFF, Data_F)
    RankPaper.text((1535, 689), Comment, C_FFFFFF, Data_F)

    if rtype:
        Part = AllData[bid]["part"]
        if int(Part) > 1:
            Part_X = 1833 - Part_F.getlength(Part) / 2
            RankPaper.text((Part_X, 552), f"{Part}P", C_EAAA7D, Part_F)
        RankPaper.text((1535, 833), Stow, C_FFFFFF, Data_F)
        RankPaper.text((1535, 977), Coin, C_FFFFFF, Data_F)
    else:
        RankPaper.text((1535, 833), Coin, C_FFFFFF, Data_F)
        RankPaper.text((1535, 977), Danmu, C_FFFFFF, Data_F)

    FixA = AllData[bid]["fix_a"]
    FixB = AllData[bid]["fix_b"]
    FixB_ = AllData[bid]["fix_b_"]
    FixC = AllData[bid]["fix_c"]
    FixP = AllData[bid]["fix_p"]
    AFix = f"×{str(round(FixP * FixA, 3))}"
    BFix = f"×{str(round(FixB * 50, 1))}" if rtype else f"×{str(round(FixB_, 1))}"
    BFix_ = f"×{str(round(FixB * 10, 2))}"
    CFix = "×20" if rtype else f"×{str(round(FixC, 2) if FixC < 50.00 else 50.00)}"
    RankPaper.text((1710, 551), AFix, C_EAAA7D, DataFix_F)
    RankPaper.text((1710, 695), BFix, C_EAAA7D, DataFix_F)
    RankPaper.text((1710, 839), CFix, C_EAAA7D, DataFix_F)

    if rtype:
        RankPaper.text((1710, 983), BFix_, C_EAAA7D, DataFix_F)
    RankPaper.text((1837, 492), ClickRank, C_EAAA7D, BiDataRank_F)
    RankPaper.text((1837, 635), CommentRank, C_EAAA7D, BiDataRank_F)
    if rtype:
        RankPaper.text((1837, 778), StowRank, C_EAAA7D, BiDataRank_F)
        RankPaper.text((1837, 921), CoinRank, C_EAAA7D, BiDataRank_F)
    else:
        RankPaper.text((1837, 778), CoinRank, C_EAAA7D, BiDataRank_F)
        RankPaper.text((1837, 921), DanmuRank, C_EAAA7D, BiDataRank_F)

    if f"av{Aid}" in InvalidList:
        RankPaper.text((980, 734), "视频已失效", C_CC0000, Invalid_F)
    RankImg.save(f"./ranking/list1/av{Aid}.png")


def SubRank(rtype):
    if rtype == 1:
        LastRankNum = int(MRank[0]["rank_from"])
        SScoreRankData = {
            int(v["score_rank"]): v
            for v in MRankData.values()
            if v["sp_type_id"] is None and int(v["score_rank"]) > LastRankNum
        }
        PageNum = 30
    elif rtype == 2:
        LastRankNum = 0
        SScoreRankData = {
            int(v["score_rank"]): v
            for v in MRankData.values()
            if v["sp_type_id"] is not None and int(v["score_rank"]) > LastRankNum
        }
        PageNum = 3
    elif rtype == 3:
        LastRankNum = 10
        SScoreRankData = {
            int(v["score_rank"]): v
            for v in BRankData.values()
            if int(v["score_rank"]) > LastRankNum
        }
        PageNum = 3
    elif rtype == 4:
        LastRankNum = 10
        SScoreRankData = {
            int(v["score_rank"]): v
            for v in GRankData.values()
            if int(v["score_rank"]) > LastRankNum
        }
        PageNum = 3
    for i in range(PageNum):
        SImg = Image.open(SUBRANKIMG) if rtype <= 2 else Image.open(SUBBANGUMIRANKIMG)
        SPaper = ImageDraw.Draw(SImg)
        for j in range(4):
            SBid_F = ImageFont.truetype(STYUANTI_SC_BOLD, 32)
            SBiDataRank_F = ImageFont.truetype(STYUANTI_SC_BOLD, 32)
            SData_F = ImageFont.truetype(STYUANTI_SC_BOLD, 40)
            SEmoji_F = ImageFont.truetype(EMOJIONE, 52)
            SLastRank_F = ImageFont.truetype(STYUANTI_SC_BOLD, 34)
            SScore_F = ImageFont.truetype(STYUANTI_SC_BOLD, 45)
            SScoreRank_F = ImageFont.truetype(HYM2GJ, 48)
            STitle_F = ImageFont.truetype(HUAWENYUANTI_BOLD, 52)
            SUnicodeA_F = ImageFont.truetype(SEGOE_UI, 52)
            SUnicodeB_F = ImageFont.truetype(SEGOE_UI_SYMBOL, 52)
            SUnicodeC_F = ImageFont.truetype(GOTHICA1, 52)
            SUnicodeD_F = ImageFont.truetype(SEGOE_UI_HISTORIC, 52)
            SUpTime_F = ImageFont.truetype(STYUANTI_SC_BOLD, 37)
            k = LastRankNum + 4 * i + j + 1
            SBid = SScoreRankData[k]["bv"]
            SClick = SScoreRankData[k]["clicks"]
            SClickRank = SScoreRankData[k]["clicks_rank"]
            SCoin = SScoreRankData[k]["yb"]
            SCoinRank = SScoreRankData[k]["yb_rank"]
            SComment = SScoreRankData[k]["comments"]
            SCommentRank = SScoreRankData[k]["comments_rank"]
            SCover = SScoreRankData[k]["pic"]
            SDanmu = SScoreRankData[k]["danmu"]
            SScore = SScoreRankData[k]["score"]
            SScoreRank = SScoreRankData[k]["score_rank"]
            SStow = SScoreRankData[k]["stows"]
            SStowRank = SScoreRankData[k]["stows_rank"]
            STitle = SScoreRankData[k]["title"]
            SUpTime = SScoreRankData[k]["cdate"]
            SLastRank = (
                ""
                if SScoreRankData[k]["last"] == "0"
                else f"上周：{SScoreRankData[k]['last']}"
            )
            SCoverFile = Resource(SBid, SCover, "pic")
            SCoverMark = Image.open(SCoverFile)
            SCoverRegion = SCoverMark.crop((0, 0) + SCoverMark.size)
            SPic = SCoverRegion.resize((336, 210), Image.Resampling.LANCZOS)
            SImg.paste(SPic, (63, 48 + j * 259))

            SNFCTitle = normalize("NFC", STitle)
            SNFCTitle = "".join([c for c in SNFCTitle if combining(c) == 0])
            SRegexTitle = re.sub(chr(65039), "", SNFCTitle)
            SRegexTitle = re.sub(COMBINING_CYRILLIC, "", SRegexTitle)
            SRegexTitle = re.sub(CONTROL, "", SRegexTitle)
            SShinkSize = 0
            while (STitle_F.getlength(SRegexTitle) + 443) > 1890:
                SShinkSize += 1
                STitle_F = ImageFont.truetype(HUAWENYUANTI_BOLD, 52 - SShinkSize)
                SEmoji_F = ImageFont.truetype(EMOJIONE, 52 - SShinkSize)
                SUnicodeA_F = ImageFont.truetype(SEGOE_UI, 52 - SShinkSize)
                SUnicodeB_F = ImageFont.truetype(SEGOE_UI_SYMBOL, 52 - SShinkSize)
                SUnicodeC_F = ImageFont.truetype(GOTHICA1, 52 - SShinkSize)
                SUnicodeD_F = ImageFont.truetype(SEGOE_UI_HISTORIC, 52 - SShinkSize)

            STitle_Y = 52 + j * 259
            STitle_X = 443
            si = 0
            STitle_Step = STitle_X
            while si < len(SRegexTitle):
                if (
                    emoji.is_emoji(SRegexTitle[si])
                    and re.match(r"[\u2640\u2642]", SRegexTitle[si]) is None
                ):
                    SPaper.text(
                        (STitle_Step, STitle_Y), SRegexTitle[si], C_6D4B2B, SEmoji_F
                    )
                    STitle_Step += SEmoji_F.getlength(SRegexTitle[si])
                elif re.match(CUNEIFORM, SRegexTitle[si]) is not None:
                    SPaper.text(
                        (
                            STitle_Step,
                            STitle_Y - SUnicodeD_F.getbbox(SRegexTitle[si])[-1] * 0.15,
                        ),
                        SRegexTitle[si],
                        C_6D4B2B,
                        SUnicodeD_F,
                    )
                    STitle_Step += SUnicodeD_F.getlength(SRegexTitle[si])
                elif re.match(SCRIPT_SIGN_SQUARE, SRegexTitle[si]) is not None:
                    SPaper.text(
                        (STitle_Step, STitle_Y),
                        SRegexTitle[si],
                        C_6D4B2B,
                        SUnicodeC_F,
                    )
                    STitle_Step += SUnicodeC_F.getlength(SRegexTitle[si])
                elif (
                    re.match(DINGBATS, SRegexTitle[si]) is not None
                    or re.match(MATHEMATICAL_ALPHANUMERIC_SYMBOLS, SRegexTitle[si])
                    is not None
                ):
                    SPaper.text(
                        (
                            STitle_Step,
                            STitle_Y - SUnicodeB_F.getbbox(SRegexTitle[si])[-1] * 0.15,
                        ),
                        SRegexTitle[si],
                        C_6D4B2B,
                        SUnicodeB_F,
                    )
                    STitle_Step += SUnicodeB_F.getlength(SRegexTitle[si])
                elif (
                    (re.match(MODIFIER_LETTER, SRegexTitle[si]) is not None)
                    or (
                        si + 1 < len(SRegexTitle)
                        and re.match(r"[0-9a-zA-Z\u4E00-\u9FA5]", SRegexTitle[si + 1])
                        is None
                        and re.match(MODIFIER_LETTER, SRegexTitle[si + 1]) is not None
                    )
                    or (re.match(MODIFIER_LETTER, SRegexTitle[si - 1]) is not None)
                ):
                    SPaper.text(
                        (STitle_Step, STitle_Y), SRegexTitle[si], C_6D4B2B, SUnicodeA_F
                    )
                    STitle_Step += SUnicodeA_F.getlength(SRegexTitle[si])
                else:
                    SPaper.text(
                        (STitle_Step, STitle_Y), SRegexTitle[si], C_6D4B2B, STitle_F
                    )
                    STitle_Step += STitle_F.getlength(SRegexTitle[si])
                si += 1

            SBid_X = 549 - SBid_F.getlength(SBid) / 2
            SPaper.text((SBid_X, 212 + j * 259), SBid, C_FFFFFF, SBid_F)
            SScore_X = 1706 - SScore_F.getlength(SScore)
            SPaper.text((SScore_X, 214 + j * 259), SScore, C_FFFFFF, SScore_F)
            SPaper.text((491, 133 + j * 259), SClick, C_6D4B2B, SData_F)
            SPaper.text((893, 133 + j * 259), SComment, C_6D4B2B, SData_F)
            if rtype > 2:
                SPaper.text((1218, 133 + j * 259), SDanmu, C_6D4B2B, SData_F)
            else:
                SPaper.text((1218, 133 + j * 259), SCoin, C_6D4B2B, SData_F)
                SPaper.text((1574, 133 + j * 259), SStow, C_6D4B2B, SData_F)
                SPaper.text((739, 138 + j * 259), SClickRank, C_BCA798, SBiDataRank_F)
                SPaper.text(
                    (1067, 138 + j * 259), SCommentRank, C_BCA798, SBiDataRank_F
                )
                SPaper.text((1748, 138 + j * 259), SStowRank, C_BCA798, SBiDataRank_F)
                SPaper.text((1390, 138 + j * 259), SCoinRank, C_BCA798, SBiDataRank_F)
            SScoreRank_X = 1856 - SScoreRank_F.getlength(SScoreRank) / 2
            SPaper.text(
                (SScoreRank_X, 214 + j * 259), SScoreRank, C_FFFFFF, SScoreRank_F
            )
            SPaper.text((820, 205 + j * 259), SUpTime, C_BCA798, SUpTime_F)
            SPaper.text((1244, 205 + j * 259), SLastRank, C_BCA798, SLastRank_F)
        if rtype == 1:
            SImg.save(f"./ranking/list2/{i+1:0>3}.png")
        elif rtype == 2:
            SImg.save(f"./ranking/list3/tv_{i+1:0>3}.png")
        elif rtype == 3:
            SImg.save(f"./ranking/list4/bangumi_{i+1:0>3}.png")
        elif rtype == 4:
            SImg.save(f"./ranking/list4/bangumi_{i+4:0>3}.png")


def Stat():
    ACata_F = ImageFont.truetype(FZY4K_GBK1_0, 43)
    ALastStat_F = ImageFont.truetype(STYUANTI_SC_BOLD, 31)
    ARank_F = ImageFont.truetype(STYUANTI_SC_BOLD, 35)
    AStat_F = ImageFont.truetype(STYUANTI_SC_BOLD, 38)
    AScore_F = ARank_F
    AImg_1 = Image.open(STATONEIMG)
    AImg_2 = Image.open(STATTWOIMG)
    AImg_3 = Image.open(STATTHREEIMG)
    APaper_1 = ImageDraw.Draw(AImg_1)
    APaper_2 = ImageDraw.Draw(AImg_2)
    APaper_3 = ImageDraw.Draw(AImg_3)
    for i in range(7):
        ACata = SRankData[2][i][0]
        ACata_X = 616 - ACata_F.getlength(ACata) / 2
        APaper_1.text((ACata_X, 221 + i * 120), SRankData[2][i][0], C_6D4B2B, ACata_F)
        AScore = format(SRankData[2][i][1], ",")
        AScore_X = 1046 - AScore_F.getlength(AScore)
        APaper_1.text((AScore_X, 221 + i * 120), AScore, C_6D4B2B, AScore_F)
        ARank = str(SRankData[2][i][2]) if len(SRankData[2][i + 7]) > 2 else "--"
        APaper_1.text((1440, 221 + i * 120), ARank, C_AC8164, ARank_F)
        if not ARank.isdigit():
            AStatPin = Image.open(UPIMG)
        elif int(ARank) > i + 1:
            AStatPin = Image.open(UPIMG)
        elif int(ARank) < i + 1:
            AStatPin = Image.open(DOWNIMG)
        elif int(ARank) == i + 1:
            AStatPin = Image.open(DRAWIMG)

        APinRegion = AStatPin.crop((0, 0) + AStatPin.size)
        APinCover = APinRegion.resize((45, 45), Image.Resampling.LANCZOS)
        AImg_1.paste(APinCover, (1500, 222 + i * 120), mask=APinCover)
    AImg_1.save("./ranking/pic/stat_1.png")
    for i in range(7):
        ACata = SRankData[2][i + 7][0]
        ACata_X = 616 - ACata_F.getlength(ACata) / 2
        APaper_2.text(
            (ACata_X, 221 + i * 120), SRankData[2][i + 7][0], C_6D4B2B, ACata_F
        )
        AScore = format(SRankData[2][i + 7][1], ",")
        AScore_X = 1046 - AScore_F.getlength(AScore)
        APaper_2.text((AScore_X, 221 + i * 120), AScore, C_6D4B2B, AScore_F)
        ARank = str(SRankData[2][i + 7][2]) if len(SRankData[2][i + 7]) > 2 else "--"
        APaper_2.text((1440, 221 + i * 120), ARank, C_AC8164, ARank_F)
        if not ARank.isdigit():
            AStatPin = Image.open(UPIMG)
        elif int(ARank) > i + 8:
            AStatPin = Image.open(UPIMG)
        elif int(ARank) < i + 8:
            AStatPin = Image.open(DOWNIMG)
        elif int(ARank) == i + 8:
            AStatPin = Image.open(DRAWIMG)
        APinRegion = AStatPin.crop((0, 0) + AStatPin.size)
        APinCover = APinRegion.resize((45, 45), Image.Resampling.LANCZOS)
        AImg_2.paste(APinCover, (1500, 222 + i * 120), mask=APinCover)
    AImg_2.save("./ranking/pic/stat_2.png")
    AClick = format(SRankData[3][0]["click"], ",")
    ACoin = format(SRankData[3][0]["yb"], ",")
    AComment = format(SRankData[3][0]["comment"], ",")
    ADanmu = format(SRankData[3][0]["danmu"], ",")
    AStow = format(SRankData[3][0]["stow"], ",")
    APaper_3.text((869 - AStat_F.getlength(AClick), 304), AClick, C_6D4B2B, AStat_F)
    APaper_3.text((869 - AStat_F.getlength(AComment), 438), AComment, C_6D4B2B, AStat_F)
    APaper_3.text((869 - AStat_F.getlength(AStow), 572), AStow, C_6D4B2B, AStat_F)
    APaper_3.text((869 - AStat_F.getlength(ADanmu), 706), ADanmu, C_6D4B2B, AStat_F)
    APaper_3.text((869 - AStat_F.getlength(ACoin), 840), ACoin, C_6D4B2B, AStat_F)
    ALastClick = format(SRankData[3][1]["click"], ",")
    ALastCoin = format(SRankData[3][1]["yb"], ",")
    ALastComment = format(SRankData[3][1]["comment"], ",")
    ALastDanmu = format(SRankData[3][1]["danmu"], ",")
    ALastStow = format(SRankData[3][1]["stow"], ",")
    APaper_3.text((1279, 313), ALastClick, C_AC8164, ALastStat_F)
    APaper_3.text((1279, 447), ALastComment, C_AC8164, ALastStat_F)
    APaper_3.text((1279, 581), ALastStow, C_AC8164, ALastStat_F)
    APaper_3.text((1279, 715), ALastDanmu, C_AC8164, ALastStat_F)
    APaper_3.text((1279, 849), ALastCoin, C_AC8164, ALastStat_F)
    for d in ["click", "comment", "stow", "danmu", "yb"]:
        if int(SRankData[3][0][d]) > int(SRankData[3][1][d]):
            AStatPin = Image.open(UPIMG)
        elif int(SRankData[3][0][d]) < int(SRankData[3][1][d]):
            AStatPin = Image.open(DOWNIMG)
        elif int(SRankData[3][0][d]) == int(SRankData[3][1][d]):
            AStatPin = Image.open(DRAWIMG)
        APinRegion = AStatPin.crop((0, 0) + AStatPin.size)
        APinCover = APinRegion.resize((45, 45), Image.Resampling.LANCZOS)
        a_i = ["click", "comment", "stow", "danmu", "yb"].index(d)
        AImg_3.paste(APinCover, (1503, 309 + a_i * 134), mask=APinCover)
    AImg_3.save("./ranking/pic/stat_3.png")


def MainRank():
    LastRankNum = int(MRank[0]["rank_from"])
    RankDataM = [
        (k, True)
        for k, v in MRankData.items()
        if v["sp_type_id"] is None and int(v["score_rank"]) <= LastRankNum
    ]
    RankDataB = [(k, False) for k, v in BRankData.items() if int(v["score_rank"]) <= 10]
    RankDataG = [(k, False) for k, v in GRankData.items() if int(v["score_rank"]) <= 10]
    RankDataH = [(k, True) for k, v in HRankData.items() if int(v["score_rank"]) <= 5]
    RankData = RankDataM + RankDataB + RankDataG + RankDataH
    list(map(Single, RankData))


def Opening():
    MTitle_F = ImageFont.truetype(HYM2GJ, 52)
    MWeek_F = ImageFont.truetype(HYM2GJ, 128)
    MTitle = f"{MRank[0]['name']}"
    MWeek = f"#{MRank[0]['id']}"
    MImg = Image.open(MAINTITLEIMG)
    MPaper = ImageDraw.Draw(MImg)
    MTitle_X = 376 - MTitle_F.getlength(MTitle) / 2
    MWeek_X = 355 - MWeek_F.getlength(MWeek) / 2
    MPaper.text((MTitle_X, 750), MTitle, C_FFFFFF, MTitle_F)
    MPaper.text((MWeek_X, 614), MWeek, C_FFFFFF, MWeek_F)
    MImg.save("./ranking/1_op/title.png")


def LongTerm():
    LTitle_F = ImageFont.truetype(HYM2GJ, 216)
    LongTerm_F = ImageFont.truetype(HANNOTATESC_W5, 45)
    LastRankNum = int(MRank[0]["rank_from"])
    LTitle = f"{LastRankNum}-21"
    LongTerm_ = f"长期作品：{LastRankNum - 30}个" if LastRankNum - 30 > 0 else "长期作品：没有"
    LImg = Image.open(LONGIMG)
    LPaper = ImageDraw.Draw(LImg)
    LTitle_X = 607 - LTitle_F.getlength(LTitle) / 2
    LongTerm__X = 607 - LongTerm_F.getlength(LongTerm_) / 2
    LPaper.text((LTitle_X, 415), LTitle, C_FFFFFF, LTitle_F)
    LPaper.text((LongTerm__X, 681), LongTerm_, C_FFFFFF, LongTerm_F)
    LImg.save("./ranking/pic/_1.png")


def History():
    HUpTime_F = ImageFont.truetype(HANNOTATESC_W5, 44)
    HCount_F = ImageFont.truetype(HANNOTATESC_W5, 45)
    HCount = f"该期集计投稿数：{format(HRank[0]['count'], ',')}"
    HUpTime = f"{HRank[0]['name']} (av{HRank[0]['wid']})"
    HImg = Image.open(HISTORYRECORDIMG)
    HPaper = ImageDraw.Draw(HImg)
    HCount_X = 607 - HCount_F.getlength(HCount) / 2
    HUpTime_X = 607 - HUpTime_F.getlength(HUpTime) / 2
    HPaper.text((HCount_X, 811), HCount, C_FFFFFF, HCount_F)
    HPaper.text((HUpTime_X, 529), HUpTime, C_FFFFFF, HUpTime_F)
    HImg.save("./ranking/pic/history.png")


def Top():
    Top_F = ImageFont.truetype(HYM2GJ, 390)
    Diff_F = ImageFont.truetype(HANNOTATESC_W5, 45)
    TopData = {
        int(v["score_rank"]): (k, v["score"])
        for k, v in MRankData.items()
        if v["sp_type_id"] is None and int(v["score_rank"]) <= 4
    }
    for t in range(3):
        TImg = Image.open(TOPIMG)
        TPaper = ImageDraw.Draw(TImg)
        Bid = TopData[t + 1][0]
        Diff = int(TopData[t + 1][1].replace(",", "")) - int(
            TopData[t + 2][1].replace(",", "")
        )
        DiffText = f"比第{t+2}名高出{format(Diff, ',')}pts."
        TPaper.text(
            (603 - Top_F.getlength(f"{t+1}") / 2, 318), f"{t+1}", C_FFFFFF, Top_F
        )
        TPaper.text(
            (609 - Diff_F.getlength(DiffText) / 2, 722), DiffText, C_FFFFFF, Diff_F
        )
        TImg.save(f"./ranking/list1/av{Bid}_.png")


def MakeYaml(file, max, min, part):
    content = json.load(open(f"./{WEEKS}_{file}.json", "r", encoding="utf-8"))
    rankfrom = content[0].get("rank_from")
    yamlcontent = []
    doorcontent = []
    for x in content:
        if x.get("info") is None and x.get("sp_type_id") != 2:
            rank = x["score_rank"] if x.get("score_rank") else x["rank"]
            name = f'av{x["wid"]}'
            length = 20
            if part in (7, 11, 15):
                length = 15
            if part == 16:
                length = 30
            if x.get("changqi"):
                length -= 10
            if rankfrom <= max:
                max = rankfrom
            if rank <= max and rank >= min:
                yamlcontent += [
                    {
                        ":rank": rank,
                        ":name": name,
                        ":length": length,
                        ":offset": 0,
                    }
                ]
                doorcontent += [
                    (
                        rank,
                        f'BV{x["bv"][2:]}',
                        x["name"],
                    )
                ]

    # print(dump(yamlcontent[::-1], sort_keys=False))
    with open(f"./ranking/list1/{WEEKS}_{part}.yml", "w") as f:
        f.write(f"---\n{dump(yamlcontent[::-1],sort_keys=False)}")

    with open(f"./{WEEKS}_rankdoor.csv", "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                {
                    "results": "主榜",
                    "results_history": "历史",
                    "guoman_bangumi": "国创",
                    "results_bangumi": "番剧",
                }.get(file)
            ]
        )
        writer.writerows(sorted(doorcontent, reverse=True))


def Main():
    MakeYaml("results", 99, 21, 5)
    MakeYaml("results", 20, 11, 9)
    MakeYaml("results", 10, 4, 13)
    MakeYaml("results", 3, 1, 16)
    MakeYaml("results_history", 5, 1, 15)
    MakeYaml("guoman_bangumi", 10, 1, 7)
    MakeYaml("results_bangumi", 10, 1, 11)
    Opening()
    LongTerm()
    History()
    MainRank()
    Stat()
    Top()
    for i in range(4):
        SubRank(i + 1)


if __name__ == "__main__":
    Main()
