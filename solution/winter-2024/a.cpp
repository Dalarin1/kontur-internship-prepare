#include <map>
#include <iostream>
#include <string>


#pragma DONE

int main(){
    int n;
    std::string inp;
    std::string res = "";
    int maxcount = 0;
    int count = 0;
    std::map<char, int> m;
    std::cin >> n;

    for(;n >= 0; n--){
        m.clear();
        count = 0;
        std::getline(std::cin, inp);
        for(auto& c : inp){
            if(m.find(c) == m.end()){
                count++;
            }
            m[c]=1;
        }
        if (count > maxcount){
            maxcount = count;
            res=inp;
        }
    }
    std::cout<<maxcount<<' '<<res<<std::endl;
    return 0;
}