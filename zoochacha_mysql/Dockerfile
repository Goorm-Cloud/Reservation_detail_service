FROM mysql:8.0

# MySQL 설정 파일 복사
COPY my.cnf /etc/mysql/conf.d/

# 초기화 스크립트 복사
COPY mysql_dump.sql /docker-entrypoint-initdb.d/

# 보안 강화를 위한 설정
RUN chmod 644 /etc/mysql/conf.d/my.cnf \
    && chmod 644 /docker-entrypoint-initdb.d/mysql_dump.sql

# 볼륨 설정
VOLUME ["/var/lib/mysql"]

# 포트 설정
EXPOSE 3306

# 컨테이너 실행 시 MySQL 서버 시작
CMD ["mysqld"] 
