
/*************************** Crete Script ******************************************************************************/

create table if not exists restaurant_comments
(
comment_id int primary key GENERATED ALWAYS AS identity,
comment varchar,
restaurant_name varchar
);

create table restaurant_point
(
point_id int primary key GENERATED ALWAYS as identity ,
speed_point smallint,
service_point smallint,
flavor_point smallint,
restaurant_name varchar
);

create table restaurant_url
(
url_id int primary key GENERATED ALWAYS as identity,
url_rst varchar
)


INSERT INTO restaurant_url(url_rst)
VALUES ('https://www.yemeksepeti.com/subway-besiktas-cihannuma-mah-istanbul')

INSERT INTO restaurant_url(url_rst)
VALUES ('https://www.yemeksepeti.com/focaccia-esenler-oruc-reis-mah-istanbul')

INSERT INTO restaurant_url(url_rst)
VALUES ('https://www.yemeksepeti.com/odul-bufe-fast-food-beylikduzu-yakuplu-mah-istanbul')


create table commentstotalbyrest
(
restaurant_name varchar(500) not null,
comment_count bigint 
)


create table commentswordcount_cswhen
(
restaurant_name varchar(500),
word varchar(500),
word_count bigint,
IsTesekkurler char(1),
IsKotu char(1),
IsMuthesem char(1),
IsBerbat char(1),
IsZehir char(1),
IsAfiyet char(1)
)

/*Spark'ın çalışması ile birlikte PostgreSQL tarafında  restaruant bazlı yorumlardaki kelime sayılarını doldurduğum tabloyu
kullanarak her restaurant için en çok tekrarlayan 10 kelimeyi bir tabloda tutuyorum.
*/
create view vw_toptenwordsbyrest as
select restaurant_name ,string_agg(word,',')as toptenwords from (
select restaurant_name,word,count ,
row_number() over (partition by restaurant_name order by count  desc) Top_Comment_Word from  
commentswordcount_cswhen ) tbl where Top_Comment_Word <=10
group by restaurant_name 


--Servis-Hız-Lezzet puanlandırmasında restaurant başına ortalama değerleri bu tabloda tutuyorum.
create view vw_avg_service_speed_flavor_point as 
select restaurant_name,round(avg(service_point)::numeric,3) as avg_service_point ,
       round(avg(speed_point)::numeric,3) as avg_speed_point ,round(avg(flavor_point)::numeric,3) as avg_flavor_point
from restaurant_point
group by restaurant_name 


--Başvuru yapan restaurant'lar için değerlendirme yapmak adına topladığım bilgilerle genel olarak sınıfılandırma yaptım.
create view vw_restaurant_loan_support_report as 
select ten.*,point.avg_service_point,point.avg_speed_point, point.avg_flavor_point,com.count,
case when ten.toptenwords like '%hızlı%' or ten.toptenwords like '%taze%' then 1 else 0 end as extra_measuring,
case when com.count<10000 then 0.20 
     when com.count>=10000 and com.count<=30000 then 0.40
     else 0.60 end as popularity_rate
from vw_toptenwordsbyrest ten 
inner join vw_avg_service_speed_flavor_point point 
on ten.restaurant_name = point.restaurant_name 
inner join commentstotalbyrest com 
on com.restaurant_name =point.restaurant_name 


--Son olarak her restaurant için bir kredi notu hesaplaması yapan sorguyu aşağıda tanımladım.
select *,(avg_service_point * 0.30 
               + avg_speed_point  * 0.30 + avg_flavor_point * 0.40 + extra_measuring + popularity_rate *0.60) :: numeric as credit_score 
from vw_restaurant_loan_support_report
