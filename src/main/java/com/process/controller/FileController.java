package com.process.controller;

import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.multipart.MultipartHttpServletRequest;
import com.process.service.CONSTANT.FilePath;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

/**
 * @author songkaiwen
 * @date 2021/1/25 3:50 下午
 */
@RestController
public class FileController {
    @PostMapping("/upload")
    @CrossOrigin(origins = "*",maxAge = 3600)
    @ResponseBody
    public Map<String, Object> uploadFile(HttpServletRequest request, HttpServletResponse response) {
        Map<String, Object> result = new HashMap<String, Object>();
        // 转型为MultipartHttpRequest：
        MultipartHttpServletRequest multipartRequest = (MultipartHttpServletRequest) request;
        // 获得文件：
        Iterator<String> fileName = ((MultipartHttpServletRequest) request).getFileNames();
        while (fileName.hasNext()){
            System.out.println(fileName.next());

        }
        MultipartFile file = multipartRequest.getFile("input-b5[]");

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

    @GetMapping("/hello")
    public String hello() {
        return "hello!";
    }
}
