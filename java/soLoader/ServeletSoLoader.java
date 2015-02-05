import javax.servlet.ServletContextEvent;
import javax.servlet.ServletContextListener;
import java.lang.reflect.Field;

@Slf4j
public class ServeletSoLoader implements ServletContextListener{

    @Override
        public void contextDestroyed(ServletContextEvent e) {
            Algo.getAlgo().ReleaseModel();
        }

    @Override
        public void contextInitialized(ServletContextEvent e) {
            try{
                log.info("algo data init start ...");
                String realPath = e.getServletContext().getRealPath("/");
                String dataPath = realPath+"/WEB-INF/data/";
                String soDir = realPath +"/WEB-INF/so/";
                addLibpath(soDir);
                log.info("lib path -> {}", System.getProperty("java.library.path"));
                Algo.getAlgo().ModelParaSetAndLoad(dataPath);
                log.info("algo data init end !!!");
            }
            catch (Exception ex){
                log.error("servlet listener start failed.", ex);
            }

        }

    private void  addLibpath(String path){
        try {
            System.setProperty("java.library.path", System.getProperty("java.library.path")
                    + ":" + path);
            Field fieldSysPath = ClassLoader.class.getDeclaredField("sys_paths");
            fieldSysPath.setAccessible(true);
            fieldSysPath.set(null, null);
        } catch (Exception e) {
            log.info("algo data init error ,e:{}",e);
        }
    }

