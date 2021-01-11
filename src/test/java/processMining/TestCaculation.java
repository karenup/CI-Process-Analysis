package processMining;

import processMining.Caculation;
import org.junit.Test;

import java.util.*;
import java.util.regex.Pattern;


/**
 * @author songkaiwen
 * @date 2021/1/6 4:13 下午
 */
public class TestCaculation {
    @Test
    public void testRead(){
        String fileName = "android_extract";
        Caculation caculation = new Caculation(fileName);
        caculation.calculate();
    }

    @Test
    public void testAnyway(){
        String str = "install.2";
        String pattern1 = ".*[a-z]2[a-z].*";
        String pattern2 = ".*[a-z].22[a-z].*";
        boolean isMatch = Pattern.matches(pattern1,str);
        System.out.println(isMatch);

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

        List<List<String>> result = caculation.sortedByStartTime(test);
        System.out.println(result);
    }

    @Test
    public void testCaculate(){
        String fileName = "testData";
        Caculation caculation = new Caculation(fileName);

        caculation.calculate();
        System.out.println(caculation.getNodeMap());
        System.out.println(caculation.getEdgeMap());
    }

}
