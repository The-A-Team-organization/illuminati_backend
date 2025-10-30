from django.db import connection
from .models import VoteTypes
from datetime import datetime
import time


class VoteTableService:

    def __init__(self, user):
        self.user = user


    @staticmethod
    def __get_vote_role_raw(user_role):

        vote_types = list(
            VoteTypes.objects
            .filter(user_role = user_role)
            .values_list('vote_type', flat = True)
        )

        return vote_types


    def get_all_votes(self):

        vote_types = self.__get_vote_role_raw(self.user.role)
        if not vote_types:
            return []

        placeholders = ','.join(['%s'] * len(vote_types))

        query = f"""
                SELECT v.id, v.name, v.vote_type
                FROM votes v
                LEFT JOIN vote_users vu
                ON v.id = vu.vote_id
                AND vu.user_id = %s
                WHERE (vu.id IS NULL OR vu.is_voted = FALSE)
                AND v.vote_type IN ({placeholders});
            """

        params = [self.user.id] + vote_types

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()

        votes_dicts = [{'id': v[0], 'name': v[1], 'vote_type': v[2]} for v in rows]

        return votes_dicts



class SendVoteService:

    def user_already_voted(self, user_id, vote_id):
        query = """
                    SELECT is_voted 
                    FROM vote_users 
                    WHERE user_id = %s 
                    AND vote_id = %s
                """

        params = [user_id, vote_id]
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()

        if rows is None or len(rows) == 0:
            return False

        else:
            return True


    def commit_choice(self, user_id, vote_id, choice):

        if choice == "AGREE":
            query = """
            
                    START TRANSACTION;
    
                    INSERT INTO vote_users(user_id, vote_id, is_voted) 
                    VALUES (%s, %s, TRUE);
                                            
                    UPDATE votes v
                    SET v.amount_of_agreed = v.amount_of_agreed + 1
                    WHERE v.id = %s;
                    
                    COMMIT;
                    """

            params = [user_id, vote_id, vote_id]

            with connection.cursor() as cursor:
                cursor.execute(query, params)

            return True


        elif choice == "DISAGREE":
            query = """
                    START TRANSACTION;
        
                    INSERT INTO vote_users(user_id, vote_id, is_voted)
                    VALUES (%s, %s, TRUE);
        
                    UPDATE votes v
                    SET v.amount_of_disagreed = v.amount_of_disagreed + 1
                    WHERE v.id = %s;
        
                    COMMIT;
                    """

            params = [user_id, vote_id, vote_id]

            with connection.cursor() as cursor:
                cursor.execute(query, params)

            return True

        return False



class PermissionService:

    def __init__(self, user):
        self.user = user


    def has_promote_permission(self):
        query = """
                SELECT up.date_of_last_promotion, up.is_promote_requested
                FROM users_promotions up
                WHERE up.user_id = %s;
                """

        params = [self.user.id]

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()

        votes_dicts = [{'date': v[0], 'send_request': v[1]} for v in rows]

        date = votes_dicts[0]['date']

        today = date.today()
        count_days = (today - date).days

        if count_days > 0 and votes_dicts[0]['send_request'] is not True:
            return True

        return False


    def has_ban_permission(self):
        query = """
            SELECT u.is_inquisitor
            FROM users u 
            WHERE u.id = %s;
        """
        params = [self.user.id]

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()

        is_inquisitor = rows[0][0]

        if is_inquisitor:
            return True

        return False