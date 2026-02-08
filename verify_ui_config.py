#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""验证 UI 配置"""

import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'source'))

from source import tool

print("=" * 60)
print("验证 UI 配置")
print("=" * 60)

ui_items = [
    ('menubar', 'ChooserBackground.png', 522, 87),
    ('panel', 'PanelBackground.png', 465, 513),
    ('movebar', 'MoveBackground.png', 516, 86),
    ('cards', '卡片', 64, 90),
]

print("\n当前配置：")
for name, desc, expected_w, expected_h in ui_items:
    config = tool.getDisplayConfig('ui', name)
    actual_w = config.get('width', 'N/A')
    actual_h = config.get('height', 'N/A')
    mode = config.get('scale_mode', 'N/A')

    status = "[OK]" if actual_w == expected_w and actual_h == expected_h else "[FAIL]"
    print(f"{status} {name:12} ({desc:25}): {actual_w:4} x {actual_h:4} (期望: {expected_w:4} x {expected_h:4}), mode={mode}")

print("\n" + "=" * 60)
