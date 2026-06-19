from __future__ import annotations

from typing import Any, Dict, List

from maibot_sdk import HookHandler, MaiBotPlugin
from maibot_sdk.types import HookMode, HookOrder

from .config import Emoji2FaceConfig

_EMOJI_TO_FACE: Dict[str, str] = {
    # 笑脸/积极
    "\U0001f600": "0",  # 😀 grin → 微笑
    "\U0001f603": "0",  # 😃 smile → 微笑
    "\U0001f604": "0",  # 😄 smile → 微笑
    "\U0001f601": "0",  # 😁 grin → 呲牙
    "\U0001f606": "14",  # 😆 laughing → 呲牙
    "\U0001f60a": "0",  # 😊 blush → 微笑
    "\U0001f60b": "2",  # 😋 yum → 色
    "\U0001f60c": "3",  # 😌 relieved → 发呆
    "\U0001f60d": "2",  # 😍 heart eyes → 色
    "\U0001f618": "52",  # 😘 kiss → 亲亲
    "\U0001f61a": "52",  # 😚 kiss → 亲亲
    "\U0001f617": "52",  # 😗 kiss → 亲亲
    "\U0001f619": "52",  # 😙 kiss → 亲亲
    "\U0001f60e": "16",  # 😎 cool → 酷
    "\U0001f929": "21",  # 🤩 star struck → 可爱
    "\U0001f973": "21",  # 🥳 party → 可爱
    "\u2764\ufe0f": "66",  # ❤️ heart → 爱心
    "\U0001f496": "66",  # 💖 sparkle heart → 爱心
    "\U0001f49c": "66",  # 💜 purple heart → 爱心
    "\U0001f49b": "66",  # 💛 yellow heart → 爱心
    "\U0001f49a": "66",  # 💚 green heart → 爱心
    "\U0001f499": "66",  # 💙 blue heart → 爱心
    "\U0001f9e1": "66",  # 🧡 orange heart → 爱心
    "\U0001f494": "67",  # 💔 broken heart → 心碎
    "\U0001f48b": "65",  # 💋 kiss mark → 嘴唇
    # 中性/普通
    "\U0001f642": "0",  # 🙂 slightly smile → 微笑
    "\U0001f610": "3",  # 😐 neutral → 发呆
    "\U0001f611": "3",  # 😑 expressionless → 发呆
    "\U0001f636": "10",  # 😶 no mouth → 闭嘴
    "\U0001f62c": "14",  # 😬 grimace → 惊讶
    "\U0001f60f": "23",  # 😏 smirk → 傲慢
    "\U0001f612": "1",  # 😒 unamused → 撇嘴
    "\U0001f644": "22",  # 🙄 roll eyes → 白眼
    # 负面
    "\U0001f61e": "15",  # 😞 disappointed → 难过
    "\U0001f61f": "15",  # 😟 worried → 难过
    "\U0001f620": "11",  # 😠 angry → 发怒
    "\U0001f621": "11",  # 😡 pout → 发怒
    "\U0001f624": "45",  # 😤 triumph → 左哼哼
    "\U0001f62d": "9",  # 😭 cry → 大哭
    "\U0001f622": "50",  # 😢 sad → 快哭了
    "\U0001f625": "49",  # 😥 disappointed → 委屈
    "\U0001f627": "50",  # 😧 anguished → 快哭了
    "\U0001f628": "53",  # 😨 fearful → 吓
    "\U0001f629": "35",  # 😩 weary → 折磨
    "\U0001f62a": "25",  # 😪 sleepy → 困
    "\U0001f62b": "36",  # 😫 tired → 衰
    "\U0001f630": "26",  # 😰 cold sweat → 惊恐
    "\U0001f631": "26",  # 😱 scream → 惊恐
    "\U0001f632": "14",  # 😲 astonished → 惊讶
    "\U0001f633": "34",  # 😳 flushed → 晕
    "\U0001f634": "8",  # 😴 sleeping → 睡
    "\U0001f635": "34",  # 😵 dizzy → 晕
    "\U0001f637": "19",  # 😷 mask → 吐
    "\U0001f923": "13",  # 🤣 rolling → 呲牙
    "\U0001f602": "14",  # 😂 joy → 惊讶
    "\U0001f924": "17",  # 🤤 drool → 饥饿
    "\U0001f971": "47",  # 🥱 yawn → 哈欠
    # 手势/动作
    "\U0001f44f": "42",  # 👏 clap → 鼓掌
    "\U0001f44d": "0",  # 👍 thumbs up → 微笑
    "\U0001f44e": "48",  # 👎 thumbs down → 鄙视
    "\U0001f44a": "38",  # 👊 fist → 敲打
    "\U0001f44b": "39",  # 👋 wave → 再见
    "\U0001f64f": "42",  # 🙏 pray → 鼓掌
    "\U0001f4aa": "30",  # 💪 biceps → 奋斗
    "\U0001f91d": "42",  # 🤝 handshake → 鼓掌
    "\U0001f64c": "42",  # 🙌 raised hands → 鼓掌
    "\U0001f450": "42",  # 👐 open hands → 鼓掌
    "\U0001f64b": "30",  # 🙋 raised hand → 奋斗
    "\u270b": "38",  # ✋ raised hand → 敲打
    "\u270c": "16",  # ✌️ victory → 酷
    "\U0001f596": "16",  # 🖖 vulcan → 酷
    # 物品/符号
    "\U0001f389": "68",  # 🎉 party → 蛋糕
    "\U0001f382": "68",  # 🎂 cake → 蛋糕
    "\U0001f381": "68",  # 🎁 gift → 蛋糕
    "\U0001f3b5": "57",  # 🎵 music → 啤酒
    "\U0001f3b6": "57",  # 🎶 notes → 啤酒
    "\u26a1": "69",  # ⚡ zap → 闪电
    "\U0001f4a5": "69",  # 💥 collision → 闪电
    "\U0001f4a3": "71",  # 💣 bomb → 炸弹
    "\U0001f4a2": "69",  # 💢 anger → 闪电
    "\U0001f4a4": "34",  # 💤 zzz → 晕
    "\U0001f4a8": "32",  # 💨 dash → 疑问
    "\U0001f4a9": "73",  # 💩 poop → 便便
    "\U0001f4a6": "40",  # 💦 sweat → 擦汗
    "\U0001f4a7": "40",  # 💧 droplet → 擦汗
    # 食物
    "\u2615": "60",  # ☕ coffee → 咖啡
    "\U0001f349": "56",  # 🍉 watermelon → 西瓜
    "\U0001f37a": "57",  # 🍺 beer → 啤酒
    "\U0001f37b": "57",  # 🍻 cheers → 啤酒
    "\U0001f354": "61",  # 🍔 burger → 饭
    "\U0001f35c": "61",  # 🍜 noodle → 饭
    "\U0001f363": "61",  # 🍣 sushi → 饭
    "\U0001f37f": "57",  # 🍿 popcorn → 啤酒
    # 动物
    "\U0001f437": "62",  # 🐷 pig → 猪头
    "\U0001f43b": "62",  # 🐻 bear → 猪头
    "\U0001f43e": "62",  # 🐾 paws → 猪头
    "\U0001f431": "21",  # 🐱 cat → 可爱
    "\U0001f436": "21",  # 🐶 dog → 可爱
    "\U0001f43c": "21",  # 🐼 panda → 可爱
    # 自然
    "\U0001f339": "63",  # 🌹 rose → 玫瑰
    "\U0001f33a": "63",  # 🌺 hibiscus → 玫瑰
    "\U0001f335": "63",  # 🌵 cactus → 玫瑰
    "\U0001f331": "63",  # 🌱 seedling → 玫瑰
    "\U0001f490": "63",  # 💐 bouquet → 玫瑰
    # 天气
    "\u2600\ufe0f": "29",  # ☀️ sun → 悠闲
    "\U0001f31e": "29",  # 🌞 sun face → 悠闲
    "\U0001f319": "29",  # 🌙 moon → 悠闲
    "\u26c5": "27",  # ⛅ cloudy → 流汗
    "\U0001f327": "27",  # 🌧️ rain → 流汗
    # 运动
    "\u26bd": "72",  # ⚽ soccer → 足球
    "\U0001f3c0": "58",  # 🏀 basketball → 篮球
    "\U0001f3d0": "59",  # 🏐 volleyball → 乒乓
    "\U0001f3be": "59",  # 🎾 tennis → 乒乓
    "\U0001f3b1": "59",  # 🎱 8ball → 乒乓
    # 其他常用
    "\U0001f514": "7",  # 🔴 bell → 闭嘴
    "\U0001f511": "7",  # 🔑 key → 闭嘴
    "\U0001f512": "7",  # 🔒 lock → 闭嘴
    "\U0001f513": "7",  # 🔓 unlock → 闭嘴
    "\U0001f308": "16",  # 🌈 rainbow → 酷
    "\U0001f31f": "16",  # 🌟 star → 酷
    "\u2728": "16",  # ✨ sparkles → 酷
    "\U0001f4f1": "32",  # 📱 phone → 疑问
    "\U0001f4de": "32",  # 📞 phone → 疑问
    "\U0001f4ac": "7",  # 💬 speech → 闭嘴
    "\u2753": "32",  # ❓ question → 疑问
    "\u2757": "14",  # ❗ exclamation → 惊讶
    "\u203c\ufe0f": "14",  # ‼️ double excl → 惊讶
}

_SORTED_EMOJI = sorted(_EMOJI_TO_FACE.keys(), key=len, reverse=True)


class Emoji2FacePlugin(MaiBotPlugin):
    config_model = Emoji2FaceConfig

    async def on_load(self) -> None:
        self.ctx.logger.info("emoji2face 插件已加载，模式: %s", self.config.convert.mode)

    async def on_unload(self) -> None:
        self.ctx.logger.info("emoji2face 插件已卸载")

    async def on_config_update(self, scope: str, config_data: dict, version: str) -> None:
        self.ctx.logger.info("emoji2face 配置已更新: %s", version)

    @HookHandler(
        "send_service.before_send",
        name="emoji_to_face",
        description="将出站消息文本中的 Unicode emoji 转为 QQ face 表情段",
        mode=HookMode.BLOCKING,
        order=HookOrder.EARLY,
    )
    async def _hook_before_send(self, **kwargs: Any) -> Dict[str, Any]:
        if not self.config.plugin.enabled:
            return {"action": "continue", "modified_kwargs": kwargs}

        mode = self.config.convert.mode
        if mode == "off":
            return {"action": "continue", "modified_kwargs": kwargs}

        max_count = self.config.convert.max_emoji_per_message
        message = kwargs.get("message")
        if not isinstance(message, dict):
            return {"action": "continue", "modified_kwargs": kwargs}

        raw = message.get("raw_message")
        if not isinstance(raw, list):
            return {"action": "continue", "modified_kwargs": kwargs}

        new_raw: List[Dict[str, Any]] = []
        remaining = max_count

        for item in raw:
            if not isinstance(item, dict):
                new_raw.append(item)
                continue

            item_type = str(item.get("type") or "").strip()
            item_data = item.get("data")

            if item_type == "text" and isinstance(item_data, str):
                parts = self._split_emoji_text(item_data, remaining)
                new_raw.extend(parts)
                # count how many face segments were added
                remaining -= sum(1 for p in parts if p.get("type") == "face")
            else:
                new_raw.append(item)

        kwargs["message"]["raw_message"] = new_raw
        return {"action": "continue", "modified_kwargs": kwargs}

    @staticmethod
    def _split_emoji_text(
        text: str, max_count: int,
    ) -> List[Dict[str, Any]]:
        if not text or max_count <= 0:
            return [{"type": "text", "data": text}] if text else []

        result: List[Dict[str, Any]] = []
        buf: List[str] = []
        count = 0
        i = 0

        while i < len(text) and count < max_count:
            matched = False
            for emoji_chars in _SORTED_EMOJI:
                if text[i:].startswith(emoji_chars):
                    if buf:
                        result.append({"type": "text", "data": "".join(buf)})
                        buf = []
                    face_id = _EMOJI_TO_FACE[emoji_chars]
                    result.append({"type": "face", "data": {"id": face_id}})
                    i += len(emoji_chars)
                    count += 1
                    matched = True
                    break
            if not matched:
                buf.append(text[i])
                i += 1

        if buf:
            result.append({"type": "text", "data": "".join(buf)})
        elif i < len(text):
            result.append({"type": "text", "data": text[i:]})

        return result


def create_plugin() -> Emoji2FacePlugin:
    return Emoji2FacePlugin()
