### 目录树层级结构 - 递归查询

1. Django ORM：
    - 层级结构不确定
    - 返回给前端的格式：子类全部放在 children 的列表中，向下嵌套
    - 使用递归查询

2. MySQL查询子类：
    - 适用于5.0(5.7.25)版本，[参考文章](https://blog.csdn.net/qq_42986107/article/details/101113098)
        - 查询所有子节点：
        ```sql
        SELECT u2.id, u2.name
        FROM (
                 SELECT @ids                                                                                 AS p_ids,
                        (SELECT @ids := GROUP_CONCAT(id) FROM index_tree WHERE FIND_IN_SET(parent_id, @ids)) AS c_ids,
                        @l := @l + 1                                                                         AS LEVEL
                 FROM index_tree,
                      (SELECT @ids := 1, @l := 0) b -- 此处为需要传递的父类id.
                 WHERE @ids IS NOT NULL
             ) u1
        JOIN index_tree u2
          ON FIND_IN_SET(u2.id, u1.p_ids) AND u2.id != 1; -- 需要包含自己, 则删掉 !=
        ```
        - 查询所有父节点:
        ```sql
        SELECT u2.id, u2.name
        FROM (
                 SELECT @id                                                                                c_ids,
                        (SELECT @id := GROUP_CONCAT(parent_id) FROM index_tree WHERE FIND_IN_SET(id, @id)) p_ids,
                        @l := @l + 1 AS                                                                    LEVEL
                 FROM index_tree,
                      (SELECT @id := '10', @l := 0) b
                 WHERE @id IS NOT NULL
             ) u1
        JOIN index_tree u2 ON u1.c_ids = u2.id;
        ```
    - 适用于8.0(8.0.26)版本:
        - cte

3. 目录树数据：
    
    ![目录树数据](../docs/index_tree.png)