#!/usr/bin/env python3
#
# Copyright 2022 Canonical Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Basic button widget.

Default button widget. Should be used by default
unless a more complex button widget is required.
"""

from typing import Union

import textual.events as events
from rich.align import Align
from rich.console import Console, ConsoleOptions, RenderResult, RenderableType
from rich.style import StyleType
from textual.message import Message
from textual.reactive import Reactive
from textual.widget import Widget


class ButtonPressedEvent(Message, bubble=True):
    """Message emitted by button to be handled by another method."""
    pass


class ButtonRenderable:
    """Button widget displayed on screen."""
    def __init__(self, label: RenderableType, style: StyleType = "") -> None:
        self.label = label
        self.style = style

    def __rich_console__(self, console: Console, opt: ConsoleOptions) -> RenderResult:
        width = opt.max_width
        height = opt.height or 1
        yield Align.center(
            self.label, vertical="middle", style=self.style, width=width, height=height
        )


class Button(Widget):
    """Method definitions and event handlers for the button class."""
    def __init__(
        self, 
        label: RenderableType, 
        name: Union[str, None] = None, 
        style: StyleType = "white on navy_blue"
    ) -> None:
        super().__init__(name=name)
        self.label = label
        self.name = name or str(label)
        self.style = style
        
    has_focus: Reactive[bool] = Reactive(False)
    mouse_over: Reactive[bool] = Reactive(False)

    async def render(self) -> RenderableType:
        """Triggers when widget is first rendered on screen."""
        return ButtonRenderable(self.label, self.style)

    async def on_focus(self, event: events.Focus) -> None:
        """Triggers when widget is focused."""
        self.has_focus = True

    async def on_blur(self, event: events.Blur) -> None:
        """Triggers when widget is unfocused."""
        self.has_focus = False

    async def on_enter(self, event: events.Enter) -> None:
        """Triggers when mouse enters widget."""
        self.mouse_over = True

    async def on_leave(self, event: events.Leave) -> None:
        """Triggers when mouse leaves widget."""
        self.mouse_over = False

    async def on_click(self, event: events.Click) -> None:
        """Triggers when widget is clicked."""
        event.prevent_default().stop()
        await self.emit(ButtonPressedEvent(self))
