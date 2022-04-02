

from queue import Empty
import scrapy

class ItemSpider(scrapy.Spider):
    name="items"

    start_urls=[
        'https://www.midsouthshooterssupply.com/dept/reloading/primers',
    ]
    
    def parse(self, response):
        
        for item in response.css('div.product'):
            stock=False
            status=item.css('.status span::text').get()

            if status == "In Stock":
                stock=True

            price=float(item.css('.price span::text').get()[1:])
            title=item.css('div a::text').get()
            manufacturer=item.css('.catalog-item-brand-item-number a::text' ).get()


#           yield{
#            'price':price,
#            'title':title,
#            'stock':stock,
#            'manufacturer':manufacturer,
#        }
        

            content_url=item.css('.product-description a::attr(href)').get()
            
            yield response.follow(content_url, dont_filter=True, callback=self.parse_page2,cb_kwargs={'price': price,'title':title,'stock':stock,'manufacturer':manufacturer})

        next_page=response.xpath("//span[@id='MainContent_dpProductsBottom']/a/@href").get()  
        if next_page is not None:
            next_page=response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_next)

    

    def parse_next(self, response):
        for item in response.css('div.product'):
            stock=False
            status=item.css('.status span::text').get()

            if status == "In Stock":
                stock=True

            price=float(item.css('.price span::text').get()[1:])
            title=item.css('div a::text').get()
            manufacturer=item.css('.catalog-item-brand-item-number a::text' ).get()
            content_url=item.css('.product-description a::attr(href)').get()
            
            yield response.follow(content_url, dont_filter=True, callback=self.parse_page2,cb_kwargs={'price': price,'title':title,'stock':stock,'manufacturer':manufacturer})
        
      
    
    def parse_page2(self, response, **kwargs):

        #description
        des_lis=response.xpath("//div[@id='description']/text()").getall()
        par=''
        for i in range(0,len(des_lis)):
            sen=des_lis[i].strip()
            par=par+"_"+sen

        #delivery
        del_lis=response.xpath("//div[@id='delivery-info']/ul/li/text()").getall()
        del_par=''
        for i in range(0,len(del_lis)):
            sen=del_lis[i].strip()
            del_par=del_par+"_"+sen

        #reviews
        rev=response.xpath("//p[@class='pr-rd-description-text/text()']").getall()
        
        if rev:
          revp='_'.join(rev)
          yield{
            'price':kwargs['price'],
            'title':kwargs['title'],
            'stock':kwargs['stock'],
            'manufacturer':kwargs['manufacturer'],
            'review':revp,
            'description':par,
            'delivery_info':del_par,


           
            }
        else:
             
            yield{
            'price':kwargs['price'],
            'title':kwargs['title'],
            'stock':kwargs['stock'],
            'manufacturer':kwargs['manufacturer'],
            'description':par,
            'delivery_info':del_par,
            }




       
        
       