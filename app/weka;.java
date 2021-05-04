package WekaDemo;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;

public class Txt2Arff {
	 static ArrayList inList=new ArrayList();
	    static String colNames[];
	    static String colTypes[];
	    static String indata[][];
	    static ArrayList clsList=new ArrayList();
	    static ArrayList disCls=new ArrayList();
	    
	    static  String res="";
	    
	 public String genTrain() throws IOException
	    {
		 
		 File fe=new File("C:/Users/Julian/Downloads/english_japanese (1).txt");
         FileInputStream fis=new FileInputStream(fe);
         byte bt[]=new byte[fis.available()];
         fis.read(bt);
         fis.close();
		 String st=new String(bt);
		 String s1[]=st.trim().split("\n");
         String col[]=s1[0].trim().split("\t");
         colNames=col;
         colTypes=s1[1].trim().split("\t");
         for(int i=2;i<s1.length;i++)
         {
             inList.add(s1[i]);
         }
         ArrayList at=new ArrayList();
         for(int i=0;i<inList.size();i++)
         {
             String g1=inList.get(i).toString();
             if(!g1.contains("?"))
             {
                 at.add(g1);
                 res=res+g1+"\n";
             }
         }
         indata=new String[at.size()][colNames.length-1];  // remove cls
     
         
         for(int i=0;i<at.size();i++)
         {
             String s2[]=at.get(i).toString().trim().split("\t");
             for(int j=0;j<s2.length-1;j++)
             {
                 indata[i][j]=s2[j].trim();                    
             }
             if(!disCls.contains(s2[s2.length-1].trim()))
                 disCls.add(s2[s2.length-1].trim());
             clsList.add(s2[s2.length-1]);
         }
	        String ar="@relation tra\n";
	        try
	        {
	            
	            for(int i=0;i<colNames.length-1;i++) // all columName which you have split and store in Colname
	            {
	            	//where yor attitude in nominal or you can say character value
	                if(colTypes[i].equals("con"))
	                    ar=ar+"@attribute "+colNames[i].trim().replace(" ","_")+" real\n";
	                else
	                {
	                	
	                	
	                	
	                    ArrayList at1=new ArrayList();
	                    for(int j=0;j<indata.length;j++) //your all numeric data
	                    {
	                        if(!at1.contains(indata[j][i].trim()))
	                            at1.add(indata[j][i].trim());
	                    }
	                    String sg1="{";
	                    for(int j=0;j<at1.size();j++)
	                    {
	                        sg1=sg1+at1.get(j).toString().trim()+",";
	                    }
	                    sg1=sg1.substring(0,sg1.lastIndexOf(","));
	                    sg1=sg1+"}";
	                    
	                    ar=ar+"@attribute "+colNames[i].trim().replace(" ", "_")+" "+sg1+"\n";
	                }
	            }
	            
	            //end of attribute
	            
	            // now adding a class Attribute 
	                        
	            ArrayList dis=new ArrayList();
	            String c1="";
	            for(int i=0;i<clsList.size();i++)
	            {
	                String g=clsList.get(i).toString().trim();
	                if(!dis.contains(g))
	                {
	                    dis.add(g);
	                    c1=c1+g+",";
	                }
	            }
	            c1=c1.substring(0, c1.lastIndexOf(","));
	            ar=ar+"@attribute class {"+c1+"}\n"; //attribute name 
	            //adding class attribute is done 
	            //now data
	            ar=ar+"@data\n";
	            
	            for(int i=0;i<indata.length;i++)
	            {
	                String g1="";
	                for(int j=0;j<indata[0].length;j++)
	                {
	                    g1=g1+indata[i][j]+",";
	                }
	                g1=g1+clsList.get(i);
	                ar=ar+g1+"\n";
	            }            
	            
	        }
	        catch(Exception e)
	        {
	            e.printStackTrace();
	        }
	        return ar;
	    }
	
	
	
	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		Txt2Arff T2A=new Txt2Arff();
		
		
		String ar1=T2A.genTrain();
		
		 File fe1=new File("C:/Users/Julian/OneDrive/Desktop/homework/tr.arff");
         FileOutputStream fos1=new FileOutputStream(fe1);
         fos1.write(ar1.getBytes());
         fos1.close();

	}

}