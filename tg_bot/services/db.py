from typing import List

import asyncpg


class Repo:
    """Db layer"""

    def __init__(self, conn: asyncpg.pool.PoolConnectionProxy) -> None:
        self.conn = conn

    async def add_user(self, tg_id: int, username: str) -> None:
        """Добавляет пользователя в базу данных"""
        await self.conn.execute(
            "INSERT INTO users(tg_id, username) VALUES ($1, $2) ON CONFLICT (tg_id) DO NOTHING",
            tg_id, username
        )
        return

    async def users_list(self) -> List[asyncpg.Record]:
        """Возвращает список всех пользователей бота"""
        users = [
            row[0]
            for row in await self.conn.fetch(
                "SELECT id FROM users",
            )
        ]
        return users

    async def get_user_subscriptions(self, tg_id: int) -> List[asyncpg.Record]:
        """Подписки пользователя"""
        subscriptions = [
            row
            for row in await self.conn.fetch(
                """
                SELECT s.id, s.service_name FROM services s
                JOIN subscriptions subs
                ON s.id = subs.service_id
                WHERE subs.user_id = (
                    SELECT id FROM users
                    WHERE tg_id = $1
                    );
                """,
                tg_id
            )
        ]

        return subscriptions

    async def add_subcription(self, tg_id: int, service_id: int) -> None:
        """Добавление подписки

        Добавляет пользователя в список рассылки по определенному
        сервису.
        """
        await self.conn.execute(
            """
            INSERT INTO subscriptions(user_id, service_id)
            VALUES (
                (SELECT id FROM users WHERE tg_id = $1),
                $2
            )
            ON CONFLICT (user_id, service_id) DO NOTHING
            """,
            tg_id, service_id
        )

    async def delete_subscription(self, tg_id: int, service_id: int) -> None:
        """Удаление подписки

        Удаляет пользователя из списка рассылки
        по определенному сервису.
        """
        await self.conn.execute(
            """
            DELETE FROM subscriptions as s
            WHERE user_id = (SELECT id FROM users WHERE tg_id = $1)
            AND service_id = $2;
            """,
            tg_id, service_id
        )

    async def get_available_services_to_subscribe(self, tg_id: int) -> List[asyncpg.Record]:
        """Доступные сервисы для подписки

        В список не включены те сервисы, на которые пользователь
        уже подписан
        """
        services = [
            row
            for row in await self.conn.fetch(
                """
                SELECT id, service_name FROM services
                WHERE services.id NOT IN (
                    SELECT service_id
                    FROM subscriptions
                    WHERE user_id = (
                        SELECT id
                        FROM users
                        WHERE tg_id = $1
                    )
                );
                """,
                tg_id,
            )
        ]

        return services

    async def increase_interactions_counter(self, command: str) -> None:
        """Счетчик

        Обновляет счетчик вызова команд по названию команды.
        """
        await self.conn.execute(
            """
            UPDATE interactions_count
            SET cnt = cnt + 1
            WHERE command = $1
            """,
            command
        )
        return
