# Final projects introduction

## 1. Background information
The project aims at analyzing the relation between Beijing house price data and subway station data as well as time. 

Dataset used:
* Subway station geological data
* House sale price data (2011-2017) 
* Rent house data price data 

## 2. Project proposal

* Assume the house sale price keep increasing from 2011 to 2017. If not, find out policy factors cause the difference. 
* Assume that the house sale price is influenced by trade time, July and August might be the highest during a year.  
* People will be likely to pay more to buy or rent a house near to a metro station. The price will decrease as the distance between house and metro station increase, e.g house price decrease 1000 RMB every KM further from metro station. 

## 3. Result representation

* Proposal 1: Assume the house sale price keep increasing from 2011 to 2017. If not, find out policy factors cause the difference. 
>The boxplot shows that the most of the time the house price keep rising, from around 20,000 to around 6000.  But two time period deserves focus. One is the dramatical increase happens from 2016 Feb, and the other is the sudden decrease from 2017 April. The result of first hypothyse is not that accurate. 

![image](https://github.com/ruobing110/final_projects/raw/master/figures/2011_2017_house_price_box_plot.jpg)
>In order to know what happens cause the rise and fall in the gram, we search the news reported and policies released at that time. According to several reports. We find out the policy which cause the variation. 
By early 2016, the Chinese government introduced a series of measures to increase property purchases, including lower taxes on home sales, limiting land sales for new development projects, and the third in a series of mortgage down payment reductions. 

From Bloomberg Business, a report on February 2016, shows that China’s central bank will allow banks to cut the minimum required mortgage down payment to 20%. And minimum down payment required for second homes cut to 30%. The policy boost people floods in property market. And the price of properties goes up quickly.

>In 2017, Beijing Municipal Government release a strict property-purchasing limitations. As there are many wealthy people trying to buy multiple property and then sell it for profit. 
This time the property-purchasing limitations aims at raise the down-payment requirements.  <br>

Beijing Municipal Government issued new rules limiting the number of homes each family can buy as the government steps up efforts to cool the property market. 
The new rules ban Beijing families who own two or more apartments and non-Beijing registered families who own one or more apartment from buying more homes. 
And the new rules allow banks to further raise the down-payment requirements for apartment buyers and raise interest rates on mortagages. 
The minimum down payment requirements was raised to 35% for first home and 60% for the second homes

* Proposal 2: Assume that the house sale price is influenced by trade time, July and August might be the highest during a year.  
>Form the bar plot, the proposal 2 is not accurate. Because of the house purchase policy changes, the house price of Beijing keeps increasing,
it makes the house sale price keep going up. Only in 2011, the house sale price is the highest in July and August. 

<div align=center>
<img src="https://github.com/ruobing110/final_projects/raw/master/figures/2011_house_price_bar_plot.jpg" height="250px" alt="" >
<img src="https://github.com/ruobing110/final_projects/raw/master/figures/2012_house_price_bar_plot.jpg" height="250px" alt="">
<img src="https://github.com/ruobing110/final_projects/raw/master/figures/2013_house_price_bar_plot.jpg" height="250px" alt="">
</div>

<div align=center>
<img src="https://github.com/ruobing110/final_projects/raw/master/figures/2014_house_price_bar_plot.jpg" height="250px" alt="">
<img src="https://github.com/ruobing110/final_projects/raw/master/figures/2015_house_price_bar_plot.jpg" height="250px" alt="" >
<img src="https://github.com/ruobing110/final_projects/raw/master/figures/2016_house_price_bar_plot.jpg" height="250px" alt="">
<img src="https://github.com/ruobing110/final_projects/raw/master/figures/2017_house_price_bar_plot.jpg" height="250px" alt="">
</div>

* Proposal 3: People will be likely to pay more to buy or rent a house near to a metro station. The price will decrease as the distance between house and metro station increase, e.g house price decrease 1000 RMB every KM further from metro station. 


>In this case, first we use the sale price dataset for a quick check to see the tendency of the house sale price. 
The blue box represents house with no subway nearby, and the orange box represents those house with a subway station in 3km distance from the houses. 
>From the box plot, the median of unit house sale price per square meters with metro is about 10,000 RMB, $1300 higher than those without a subway station.

![image](https://github.com/ruobing110/final_projects/raw/master/figures/2011_2017_house_price_influenced_by_subway.jpg)

>The histogram of house rent price shows that there are two concentrated house rent price. 
One is around 3500 RMB, about 500 dollars, and the other one is about 5700. This is because the difference of house area. 
The house area ranges from 40 m2 to more than 150 m2. 


<div align=center>
<img src="https://github.com/ruobing110/final_projects/raw/master/figures/house_price_histogram_with_mark.png" height="250px" alt="" >
</div>

In this subway dataset and house rent dataset,  the longitude and latitude for each house and subway station are provided. 
After calculation , we get which subway station is the nearest one for a house and the distance between the house and its nearest metro station. 

And the boxplot is the overiew of the nearest distance and average rent
The horizontal  axis represent the distance within 1 kilometer, the distance between 1 and two km and so on. 
The y axis represent the average rent by square meters. And from this plot, as the distance increase, the rent per square meters decrease. 
>The calculation result shows the distance between house and metro station, for which distance within 1km, the average rents per square meters is 95, in total 4697 each house. 
While the distance between 1km and 2 km, the average price decrease to 70 per square meters, in total 4024 each house .  

<div align=center>
<img src="https://github.com/ruobing110/final_projects/raw/master/figures/house_sale_price_with_metro_distance.jpg" height="250px" alt="" >
</div>

We draw a regplot to show the regression model. The line in the plot shows that. As the distance increase, each m will cause the 0.02422 decrease in price. 
The intercection for this line is 107.  which means  the unit rent price decrease 242 RMB each km further from nearest metro station.
As there are so many points so we draw another plot, hexplot. From this plot we can see, a lot of points gathered in the bottom left corner. 
Most house rent is about 100 yuan per square meters and the nearest distance from subway stations within 1 kilometers.


<div align=center>
<img src="https://github.com/ruobing110/final_projects/raw/master/figures/distance_average_price.jpg" height="250px" alt="">
<img src="https://github.com/ruobing110/final_projects/raw/master/figures/hexplot.jpg" height="250px" alt="" >
</div>

























