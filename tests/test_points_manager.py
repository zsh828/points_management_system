from src.points_manager import PointsManager
import pytest


class TestPointsManager:
    """测试 PointsManager 类的功能"""

    def setup_method(self):
        """每个测试方法执行前重置状态"""
        self.manager = PointsManager()

    # --- 测试添加用户和积分计算 ---

    def test_add_new_user(self):
        """测试添加新用户并计算积分"""
        points = self.manager.add_user("user1", 100.5)
        assert points == 100  # 1元=1分，向下取整或直接取整数部分，通常积分是整数

    def test_add_existing_user_accumulate(self):
        """测试已有用户累加积分"""
        self.manager.add_user("user1", 100)
        points = self.manager.add_user("user1", 50)
        assert points == 150

    def test_add_user_zero_amount(self):
        """测试消费金额为0时"""
        points = self.manager.add_user("user2", 0)
        assert points == 0

    def test_add_user_negative_amount_raises_or_handles(self):
        """测试负数消费金额的处理逻辑（根据需求，通常不允许负数，但此处模拟业务逻辑）"""
        # 假设业务上允许负数（退款），则积分会减少
        self.manager.add_user("user3", 100)
        points = self.manager.add_user("user3", -20)
        assert points == 80

    # --- 测试查询积分 ---

    def test_get_points_existing_user(self):
        """测试查询已存在用户的积分"""
        self.manager.add_user("user1", 100)
        assert self.manager.get_points("user1") == 100

    def test_get_points_non_existing_user(self):
        """测试查询不存在的用户，应返回0"""
        assert self.manager.get_points("non_existent") == 0

    def test_get_points_empty_user_id_raises(self):
        """测试传入空字符串作为用户ID应抛出异常"""
        with pytest.raises(ValueError, match="User ID cannot be empty"):
            self.manager.get_points("")

    def test_get_points_none_user_id_raises(self):
        """测试传入None作为用户ID应抛出异常"""
        with pytest.raises(ValueError, match="User ID cannot be empty"):
            self.manager.get_points(None)

    # --- 测试积分兑换 ---

    def test_redeem_points_success(self):
        """测试成功兑换积分"""
        self.manager.add_user("user1", 100)
        result = self.manager.redeem_points("user1", 30)
        assert result is True
        assert self.manager.get_points("user1") == 70

    def test_redeem_points_insufficient_funds(self):
        """测试积分不足时兑换失败"""
        self.manager.add_user("user1", 10)
        result = self.manager.redeem_points("user1", 20)
        assert result is False
        # 积分不应改变
        assert self.manager.get_points("user1") == 10

    def test_redeem_points_non_existing_user(self):
        """测试不存在的用户兑换积分，应返回False"""
        result = self.manager.redeem_points("non_existent", 10)
        assert result is False

    def test_redeem_points_zero_raises(self):
        """测试兑换0积分应抛出异常"""
        with pytest.raises(ValueError, match="Points to redeem must be positive"):
            self.manager.redeem_points("user1", 0)

    def test_redeem_points_negative_raises(self):
        """测试兑换负数积分应抛出异常"""
        with pytest.raises(ValueError, match="Points to redeem must be positive"):
            self.manager.redeem_points("user1", -5)

    def test_redeem_all_points(self):
        """测试兑换所有积分"""
        self.manager.add_user("user1", 100)
        result = self.manager.redeem_points("user1", 100)
        assert result is True
        assert self.manager.get_points("user1") == 0

    # --- 测试排行榜 ---

    def test_get_leaderboard_basic(self):
        """测试基本排行榜功能"""
        self.manager.add_user("alice", 100)
        self.manager.add_user("bob", 200)
        self.manager.add_user("charlie", 150)
        
        leaderboard = self.manager.get_leaderboard(top_n=3)
        
        assert len(leaderboard) == 3
        assert leaderboard[0]["user_id"] == "bob"
        assert leaderboard[0]["points"] == 200
        assert leaderboard[1]["user_id"] == "charlie"
        assert leaderboard[1]["points"] == 150
        assert leaderboard[2]["user_id"] == "alice"
        assert leaderboard[2]["points"] == 100

    def test_get_leaderboard_top_n_larger_than_users(self):
        """测试请求的Top N大于实际用户数"""
        self.manager.add_user("alice", 100)
        self.manager.add_user("bob", 200)
        
        leaderboard = self.manager.get_leaderboard(top_n=10)
        
        assert len(leaderboard) == 2
        assert leaderboard[0]["user_id"] == "bob"

    def test_get_leaderboard_empty_users(self):
        """测试没有用户时的排行榜"""
        leaderboard = self.manager.get_leaderboard(top_n=5)
        assert leaderboard == []

    def test_get_leaderboard_invalid_top_n(self):
        """测试无效的Top N参数"""
        with pytest.raises(ValueError, match="top_n must be at least 1"):
            self.manager.get_leaderboard(top_n=0)
            
        with pytest.raises(ValueError, match="top_n must be at least 1"):
            self.manager.get_leaderboard(top_n=-5)

    def test_leaderboard_sorting_order(self):
        """测试排行榜是否正确按积分降序排列"""
        self.manager.add_user("u1", 50)
        self.manager.add_user("u2", 50)  # 积分相同
        self.manager.add_user("u3", 100)
        
        leaderboard = self.manager.get_leaderboard(top_n=3)
        
        # u3 应该排第一
        assert leaderboard[0]["user_id"] == "u3"
        assert leaderboard[0]["points"] == 100
        
        # u1 和 u2 积分相同，顺序取决于sorted的实现稳定性，但都应在u3之后
        assert leaderboard[1]["points"] == 50
        assert leaderboard[2]["points"] == 50