__author__ = 'marble_xu'

import pygame as pg
from datetime import datetime
from .. import tool
from .. import constants as c
from ..language import LANG
from ..network import NETWORK


class GameReportScreen(tool.State):
    """游戏报告页面，显示最终分数、排名和击杀统计"""

    def __init__(self):
        tool.State.__init__(self)
        self.score = 0
        self.rank = None
        self.game_duration = 0
        self.zombies_killed = {}
        self.leaderboard = []
        self.is_offline = False

        # 按钮位置
        self.export_button_rect = pg.Rect(100, 520, 150, 40)
        self.play_again_button_rect = pg.Rect(325, 520, 150, 40)
        self.exit_button_rect = pg.Rect(550, 520, 150, 40)

    def startup(self, current_time, persist):
        self.persist = persist
        self.game_info = self.persist
        self.start_time = current_time

        # 从 game_info 获取游戏数据
        self.score = self.game_info.get('final_score', 0)
        self.game_duration = self.game_info.get('game_duration', 0)
        self.zombies_killed = self.game_info.get('zombies_killed', {})
        self.is_offline = self.game_info.get('is_offline', True)
        self.rank = None
        self.leaderboard = []

        # 如果是在线模式，提交成绩并获取排行榜
        if not self.is_offline:
            try:
                player_id = self.game_info.get('player_id')
                if player_id:
                    # 提交成绩
                    result = NETWORK.submit_score(
                        player_id,
                        self.score,
                        self.game_duration,
                        self.zombies_killed
                    )
                    self.rank = result.get('rank')

                    # 获取排行榜
                    self.leaderboard = NETWORK.get_leaderboard(10)
            except Exception as e:
                print(f'Failed to submit score or get leaderboard: {e}')
                self.is_offline = True

    def update(self, surface, current_time, mouse_pos, mouse_click, events):
        self.current_time = current_time

        # 处理鼠标点击
        if mouse_pos and mouse_click[0]:
            self.handle_mouse_click(mouse_pos)

        # 绘制页面
        self.draw(surface)

    def handle_mouse_click(self, mouse_pos):
        """处理鼠标点击"""
        # 导出截图
        if self.export_button_rect.collidepoint(mouse_pos):
            self.export_screenshot()

        # 再来一局
        if self.play_again_button_rect.collidepoint(mouse_pos):
            self.done = True
            self.next = c.LEVEL

        # 退出游戏
        if self.exit_button_rect.collidepoint(mouse_pos):
            pg.event.post(pg.event.Event(pg.QUIT))

    def export_screenshot(self):
        """导出截图"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'game_report_{timestamp}.png'
        pg.image.save(pg.display.get_surface(), filename)
        print(f'Screenshot saved: {filename}')

    def draw(self, surface):
        """绘制游戏报告页面"""
        # 填充背景
        surface.fill(c.NAVYBLUE)

        # 绘制标题
        title_font = pg.font.SysFont('SimHei', 40)
        title_text = title_font.render(LANG.get('report_title'), True, c.GOLD)
        title_rect = title_text.get_rect()
        title_rect.centerx = c.SCREEN_WIDTH // 2
        title_rect.y = 20
        surface.blit(title_text, title_rect)

        # 绘制最终分数
        score_font = pg.font.SysFont('SimHei', 32)
        score_text = score_font.render(f"{LANG.get('report_final_score')}{self.score}", True, c.WHITE)
        surface.blit(score_text, (50, 80))

        # 绘制排名
        if self.is_offline:
            rank_text = score_font.render(LANG.get('report_offline'), True, c.RED)
        elif self.rank:
            rank_display = LANG.get('report_rank_format').format(self.rank)
            rank_text = score_font.render(f"{LANG.get('report_rank')}{rank_display}", True, c.WHITE)
        else:
            rank_text = score_font.render(f"{LANG.get('report_rank')}{LANG.get('report_no_rank')}", True, c.WHITE)
        surface.blit(rank_text, (50, 120))

        # 绘制游戏时长
        duration_seconds = self.game_duration // 1000
        duration_text = score_font.render(
            f"{LANG.get('report_duration')}{duration_seconds} {LANG.get('seconds')}",
            True, c.WHITE
        )
        surface.blit(duration_text, (50, 160))

        # 绘制击杀统计标题
        kills_title_font = pg.font.SysFont('SimHei', 28)
        kills_title = kills_title_font.render(LANG.get('report_kills_title'), True, c.GOLD)
        surface.blit(kills_title, (50, 210))

        # 绘制各类僵尸击杀统计
        kill_font = pg.font.SysFont('SimHei', 22)
        y_offset = 250
        zombie_name_map = {
            c.NORMAL_ZOMBIE: 'zombie_normal',
            c.CONEHEAD_ZOMBIE: 'zombie_conehead',
            c.BUCKETHEAD_ZOMBIE: 'zombie_buckethead',
            c.FLAG_ZOMBIE: 'zombie_flag',
            c.NEWSPAPER_ZOMBIE: 'zombie_newspaper',
        }

        for zombie_type, count in self.zombies_killed.items():
            if count > 0:
                zombie_name = LANG.get(zombie_name_map.get(zombie_type, zombie_type))
                score_value = c.ZOMBIE_SCORES.get(zombie_type, 0)
                total_score = count * score_value
                kill_text = kill_font.render(
                    f"{zombie_name}: {count} × {score_value} = {total_score} {LANG.get('points')}",
                    True, c.WHITE
                )
                surface.blit(kill_text, (70, y_offset))
                y_offset += 30

        # 绘制排行榜（右侧）
        if not self.is_offline and self.leaderboard:
            leaderboard_title_font = pg.font.SysFont('SimHei', 28)
            leaderboard_title = leaderboard_title_font.render(LANG.get('report_leaderboard'), True, c.GOLD)
            surface.blit(leaderboard_title, (450, 210))

            leaderboard_font = pg.font.SysFont('SimHei', 20)
            y_offset = 250
            for i, entry in enumerate(self.leaderboard[:10], 1):
                name = entry.get('name', 'Unknown')
                score = entry.get('score', 0)
                rank_text = leaderboard_font.render(f"{i}. {name}: {score}", True, c.WHITE)
                surface.blit(rank_text, (450, y_offset))
                y_offset += 28

        # 绘制按钮
        button_font = pg.font.SysFont('SimHei', 22)

        # 导出截图按钮
        pg.draw.rect(surface, c.SKY_BLUE, self.export_button_rect)
        pg.draw.rect(surface, c.WHITE, self.export_button_rect, 2)
        export_text = button_font.render(LANG.get('report_export'), True, c.WHITE)
        export_rect = export_text.get_rect()
        export_rect.center = self.export_button_rect.center
        surface.blit(export_text, export_rect)

        # 再来一局按钮
        pg.draw.rect(surface, c.GREEN, self.play_again_button_rect)
        pg.draw.rect(surface, c.WHITE, self.play_again_button_rect, 2)
        play_again_text = button_font.render(LANG.get('report_play_again'), True, c.BLACK)
        play_again_rect = play_again_text.get_rect()
        play_again_rect.center = self.play_again_button_rect.center
        surface.blit(play_again_text, play_again_rect)

        # 退出游戏按钮
        pg.draw.rect(surface, c.RED, self.exit_button_rect)
        pg.draw.rect(surface, c.WHITE, self.exit_button_rect, 2)
        exit_text = button_font.render(LANG.get('report_exit'), True, c.WHITE)
        exit_rect = exit_text.get_rect()
        exit_rect.center = self.exit_button_rect.center
        surface.blit(exit_text, exit_rect)
