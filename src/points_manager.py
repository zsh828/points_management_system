class PointsManager:
    """
    用户积分管理器类。
    
    功能：
    1. 添加用户并根据消费金额自动计算积分（1元=1分）
    2. 根据用户ID查询积分
    3. 积分兑换（消耗积分）
    4. 获取积分排行榜（Top N）
    """

    def __init__(self):
        # 存储用户积分，key为用户ID，value为当前积分
        self.user_points = {}

    def add_user(self, user_id: str, amount: float) -> int:
        """
        添加用户并根据消费金额增加积分。
        
        Args:
            user_id (str): 用户唯一标识
            amount (float): 消费金额
            
        Returns:
            int: 该用户当前的总积分
        """
        if user_id in self.user_points:
            # 如果用户已存在，累加积分
            points_earned = int(amount)
            self.user_points[user_id] += points_earned
        else:
            # 新用户，初始化积分
            points_earned = int(amount)
            self.user_points[user_id] = points_earned
            
        return self.user_points[user_id]

    def get_points(self, user_id: str) -> int:
        """
        根据用户ID查询当前积分。
        
        Args:
            user_id (str): 用户唯一标识
            
        Returns:
            int: 用户当前积分，若用户不存在则返回0
            
        Raises:
            ValueError: 如果user_id为空或None
        """
        if not user_id:
            raise ValueError("User ID cannot be empty")
            
        return self.user_points.get(user_id, 0)

    def redeem_points(self, user_id: str, points_to_redeem: int) -> bool:
        """
        积分兑换，消耗指定积分。
        
        Args:
            user_id (str): 用户唯一标识
            points_to_redeem (int): 要消耗的积分数量
            
        Returns:
            bool: 兑换是否成功。如果积分不足或用户不存在，返回False。
            
        Raises:
            ValueError: 如果points_to_redeem小于等于0
        """
        if points_to_redeem <= 0:
            raise ValueError("Points to redeem must be positive")
            
        current_points = self.user_points.get(user_id, 0)
        
        if current_points >= points_to_redeem:
            self.user_points[user_id] -= points_to_redeem
            return True
        else:
            return False

    def get_leaderboard(self, top_n: int = 10) -> list:
        """
        获取积分排行榜。
        
        Args:
            top_n (int): 返回前N名用户，默认为10
            
        Returns:
            list: 包含字典的列表，每个字典包含 'user_id' 和 'points'，按积分降序排列
        """
        if top_n < 1:
            raise ValueError("top_n must be at least 1")
            
        # 将字典转换为列表并按积分降序排序
        sorted_users = sorted(
            self.user_points.items(),
            key=lambda item: item[1],
            reverse=True
        )
        
        # 取前 top_n 名
        result = []
        for user_id, points in sorted_users[:top_n]:
            result.append({
                "user_id": user_id,
                "points": points
            })
            
        return result