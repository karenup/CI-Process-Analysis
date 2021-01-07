package processMining;

import dataProcess.Caculation;
import org.junit.Test;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.List;


/**
 * @author songkaiwen
 * @date 2021/1/6 4:13 下午
 */
public class TestCaculation {
    @Test
    public void testRead(){
        String fileName = "android_extract";
        Caculation caculation = new Caculation(fileName);
        caculation.caculate();
    }

    @Test
    public void testAnyway(){
        System.out.println();
    }

    @Test
    public void testConvert2Date(){
        String fileName = "android_extract";
        Caculation caculation = new Caculation(fileName);
        Long d = caculation.convert2Date("2015/5/7 7:34:13");
        System.out.println(d);
    }

    @Test
    public void testSortedByStartTime(){
        String fileName = "android_extract";
        Caculation caculation = new Caculation(fileName);

        List<String> test1 = Arrays.asList("35626102","commit","2014/8/1 8:38:00","nan");
        List<String> test2 = Arrays.asList("35626102","push","2014/10/18 12:15:00","2014/9/18 12:13:00");
        List<String> test3 = Arrays.asList("35626102","git","nan","2014/9/18 12:14:00");
        List<String> test4 = Arrays.asList("35626102","before_install","2014/9/18 12:13:00","2014/9/18 12:14:00");
        List<String> test5 = Arrays.asList("35626102","script","2014/9/18 12:14:00","2014/9/18 12:15:00");
        List<String> test6 = Arrays.asList("35626102","passed","2014/9/18 12:15:00","2014/9/18 12:15:00");

        List<List<String>> test = new ArrayList<>();
        test.add(test1);
        test.add(test2);
        test.add(test3);
        test.add(test4);
        test.add(test5);
        test.add(test6);

        List<List<String>> newTest = test.stream()
                .sorted((x, y) -> {
                    Long xTime = null;
                    Long yTime = null;
                    if(x.get(2).equals("nan")){
                        xTime = 0L;
                    }else if(y.get(2).equals("nan")) {
                        yTime = 0L;
                    }else {
                        xTime = caculation.convert2Date(x.get(2));
                        yTime = caculation.convert2Date(y.get(2));
                    }
                    if(Long.compare(xTime,0L) || Long.compare(yTime, 0L)){
                        return
                    }
                });
        for(List<String> s: newTest){
            System.out.println(s.get(1));
        }

    }
}
