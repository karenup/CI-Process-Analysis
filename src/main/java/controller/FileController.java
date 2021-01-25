package controller;

import jdk.nashorn.internal.objects.Global;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.multipart.MultipartHttpServletRequest;
import service.CONSTANT.FilePath;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Map;

/**
 * @author songkaiwen
 * @date 2021/1/25 3:50 下午
 */
@Controller
public class FileController {
    @PostMapping("/upload")
    @ResponseBody
    public Map<String, Object> uploadFile(HttpServletRequest request, HttpServletResponse response) {
        Map<String, Object> result = new HashMap<String, Object>();
        // 转型为MultipartHttpRequest：
        MultipartHttpServletRequest multipartRequest = (MultipartHttpServletRequest) request;
        // 获得文件：
        MultipartFile file = multipartRequest.getFile("file");
        try  {
            if (!(file.getOriginalFilename() == null || "".equals(file.getOriginalFilename()))) {
                //获取你要上传的系统盘符
                String filePath = FilePath.outputPath;
                File tempFile = new File(filePath);
                if (!tempFile.exists())
                {
                    tempFile.mkdirs();
                }
                // 对文件进行存储处理
                byte[] bytes = file.getBytes();
                Path path = Paths.get(filePath, "\\" + file.getOriginalFilename());
                Files.write(path, bytes);
                result.put("path",filePath+"/"+file.getOriginalFilename());
                result.put("msg", "上传成功！");
                result.put("result", true);
            }
        } catch (IOException e) {
            result.put("msg", "上传失败，错误异常");
            result.put("result", false);
            e.printStackTrace();
        } catch (Exception e1) {
            e1.printStackTrace();
        }
        return result;
    }
}
