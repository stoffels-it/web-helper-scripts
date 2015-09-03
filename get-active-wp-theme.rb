require "nokogiri"
require "open-uri"

searchstring = "wp-content/themes/"
filename = "url-list.txt"

File.read(filename).each_line do|wpsite|
    if wpsite != "" and wpsite != "#" and wpsite != " " and wpsite != "\n"
        begin
            doc = Nokogiri::HTML(wpsite)
        rescue
            puts "Url could not be opened: #{wpsite}"
        else
            puts "Url called successfully: #{wpsite}"
            links = doc.xpath("//link[contains(@href, '#{searchstring}')]")
            links.each do |test|
                theme = test.to_s[/#{searchstring}(.*?)\//, 1]
                if theme != ""
                    puts "Theme is: #{theme}"
                    break
                end
            end
        end
    end
end
