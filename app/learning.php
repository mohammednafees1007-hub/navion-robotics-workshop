<?php
// All guided actions are extracted from the same chapter source as the manual.
function guideSteps(string $mode):array {
 global $chapterMap;
 $route=['kit','assembly','software','serial','wiring','motor-test'];
 if($mode!=='remote')$route[]='sensors';
 $route[]=$mode;$route[]='shutdown';$steps=[];
 foreach($route as $slug){
  $body=bodyFor($slug);
  preg_match_all('~<section class="instruction"[^>]*>.*?</section>~s',$body,$matches);
  if(!$matches[0]){$steps[]=['id'=>$slug,'slug'=>$slug,'title'=>$chapterMap[$slug]['title'],'html'=>$body,'context'=>''];continue;}
  $context=preg_replace('~<section class="instruction"[^>]*>.*?</section>~s','',$body);
  $context=preg_replace('~<details class="source-code">.*?</details>~s','',$context);
  foreach($matches[0] as $i=>$html){preg_match('~<h3[^>]*>(.*?)</h3>~s',$html,$title);$steps[]=['id'=>$slug.'-'.($i+1),'slug'=>$slug,'title'=>strip_tags($title[1]??$slug),'html'=>$html,'context'=>$context];}
 }
 return $steps;
}
function searchManual(string $query):array {
 global $chapters;$results=[];
 $synonyms=['no port'=>'COM','only moves briefly'=>'800','backward'=>'reversed','brownout'=>'resets','line stops'=>'stops','GPIO39'=>'39'];
 $term=$synonyms[strtolower($query)]??$query;
 if($term==='')return [];
 foreach($chapters as $c){
  $body=bodyFor($c['slug']);
  $sections=preg_split('~(?=<h[23] id=")~',$body);
  foreach($sections as $section){$plain=html_entity_decode(strip_tags($section),ENT_QUOTES,'UTF-8');$at=stripos($plain,$term);if($at===false)continue;
   preg_match('~<h[23] id="([^"]+)">(.*?)</h[23]>~s',$section,$h);
   $results[]=['url'=>'?page=lesson&slug='.$c['slug'].(isset($h[1])?'#'.$h[1]:''),'title'=>$c['title'].(isset($h[2])?' · '.strip_tags($h[2]):''),'excerpt'=>substr($plain,max(0,$at-65),210)];
   if(count($results)>=30)return $results;
  }
 }return $results;
}
