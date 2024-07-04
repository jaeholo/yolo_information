graph TD
    BuZhou06_19 -->|CVWRunResult::EM_OK| BuZhou06_24
    BuZhou06_19 -->|CVWRunResult::EM_NOK| Exception

    BuZhou06_24 -->|Choose == 1 or Choose == 2 or Choose == 3 or Choose == 8| BuZhou06_25
    BuZhou06_24 -->|Choose == 4 or Choose == 5 or Choose == 6 or Choose == 7 or Choose == 0| Exception

    Call_19 --> BuZhou06_25

    BuZhou06_25 -->|CVWRunResult::EM_OK| BuZhou06_6
    BuZhou06_25 -->|CVWRunResult::EM_NOK| BuZhou06_26

    BuZhou06_26 --> Exception

    BuZhou06_6 -->|CVWRunResult::EM_OK| BuZhou06_21
    BuZhou06_6 -->|CVWRunResult::EM_NOK| Exception

    BuZhou06_21 -->|CVWRunResult::EM_OK| XuanZe06_9
    BuZhou06_21 -->|CVWRunResult::EM_NOK| Exception

    XuanZe06_9 -->|Choose == 1| BuZhou06_5
    XuanZe06_9 -->|Choose == 2| BuZhou06_22
    XuanZe06_9 -->|Choose == 3 or Choose == 4 or Choose == 5 or Choose == 6 or Choose == 7 or Choose == 0| Exception

    XuanZe06_15 -->|Choose == 1| BuZhou06_5
    XuanZe06_15 -->|Choose == 2| BuZhou06_22
    XuanZe06_15 -->|Choose == 3| BuZhou06_20
    XuanZe06_15 -->|Choose == 4 or Choose == 5 or Choose == 6 or Choose == 7 or Choose == 0| Exception

    BuZhou06_20 --> Exception

    BuZhou06_22 -->|Choose == 1| BuZhou06_16
    BuZhou06_22 -->|Choose == 2| BuZhou06_17
    BuZhou06_22 -->|Choose == 3 or Choose == 4 or Choose == 5 or Choose == 6 or Choose == 7 or Choose == 0| Exception

    BuZhou06_5 -->|Choose == 1| BuZhou06_16
    BuZhou06_5 -->|Choose == 2 or Choose == 3 or Choose == 4 or Choose == 5 or Choose == 6 or Choose == 7 or Choose == 0| Exception

    BuZhou06_17 -->|CVWRunResult::EM_OK| XuanZe06_8
    BuZhou06_17 -->|CVWRunResult::EM_NOK| Exception

    BuZhou06_16 -->|CVWRunResult::EM_OK| XuanZe06_8
    BuZhou06_16 -->|CVWRunResult::EM_NOK| Exception

    XuanZe06_8 -->|Choose == 8| XuanZe06_15
    XuanZe06_8 -->|Choose == 1 or Choose == 2 or Choose == 3 or Choose == 4 or Choose == 5 or Choose == 6 or Choose == 7 or Choose == 0| Exception

    Exception[Exception/End]
