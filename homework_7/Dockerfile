FROM postgres
EXPOSE 5432:5432
ENV POSTGRES_PASSWORD=root
ENV POSTGRES_USER=root
ENV POSTGRES_DB=shop
COPY shop.sql /
CMD postgres start
CMD <./shop.sql