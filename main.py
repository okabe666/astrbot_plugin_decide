from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import random
import re

@register("helloworld", "YourName", "一个简单的 Hello World 插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
        pass

    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("helloworld")
    async def helloworld(self, event: AstrMessageEvent):
        """这是一个 hello world 指令""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)
        yield event.plain_result(f"Hello, {user_name}, 你发了 {message_str}!") # 发送一条纯文本消息

    @filter.command("骰子")
    async def dice(self, event: AstrMessageEvent, n: int = 1):
        """骰子指令：/骰子 3 或 /骰子3
        支持两种形式的参数传入，若同时存在解析优先级以消息中匹配到的数字为准。"""
        msg = event.message_str or ""
        # 尝试解析附着在指令后的数字，如 "/骰子3" 或 "骰子3"
        m = re.search(r"骰子\s*(\d+)", msg)
        if m:
            try:
                n = int(m.group(1))
            except Exception:
                pass

        if n < 1:
            yield event.plain_result("数量必须至少为 1。")
            return
        if n > 100:
            yield event.plain_result("数量太大了，请不要超过 100。")
            return

        rolls = [random.randint(1, 6) for _ in range(n)]
        total = sum(rolls)
        parity = "双数" if total % 2 == 0 else "单数"
        user_name = event.get_sender_name()
        if n <= 5:
            rolls_str = ", ".join(map(str, rolls))
            yield event.plain_result(f"{user_name} 掷了 {n} 个骰子：[{rolls_str}]，合计 {total}，{parity}。")
        else:
            yield event.plain_result(f"{user_name} 掷了 {n} 个骰子，合计 {total}，{parity}。")

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
        pass
