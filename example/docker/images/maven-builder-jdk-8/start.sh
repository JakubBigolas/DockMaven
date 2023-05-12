start_script=`date +%s`



PROJECT_DIR=$(ls /usr/src/external)

echo "project sources sync"
rsync -vru --delete /usr/src/external/$PROJECT_DIR /usr/src/mymaven

echo "change context directory to project"
cd ./$PROJECT_DIR

echo "build project"
$BUILD_CMD $BUILD_PROFILES

echo "remove previous build"
rm -rfv /builds/*

echo "exporting target files"
cp .$TARGET_DIR/$APP_NAME /builds

echo "cleaning workspace"
mvn clean >> clean.log



export end_script=`date +%s`;                                                       
export diff=`expr $end_script - $start_script`;                                     
export hrs=`expr $diff / 360`;                                                      
export min=`expr $diff / 60`;                                                       
export sec=`expr $diff % 60`;                                                       
echo $PROJECT_DIR build time: `printf %02d $hrs`:`printf %02d $min`:`printf %02d $sec`;

