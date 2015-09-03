require "nokogiri"
require "open-uri"

searchstring = "wp-content/themes/"
filename = "url-list.txt"

File.read(filename).each_line do|wpsite|
    if wpsite != "" and wpsite[0] != "#" and wpsite[0] != " " and wpsite[0] != "\n"
        begin
            doc = Nokogiri::HTML(open(wpsite))
        rescue
            puts "url could not be opened: #{wpsite}"
        else
            puts "url called successfully: #{wpsite}"
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
