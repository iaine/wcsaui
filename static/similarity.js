/**
* Module to encapsulate the similarity algorithms and mark up
*/

var setOperations = function() {

  /**
  *  Method to provide the set union of a list of sets
  */
  function calculateSetUnion(listOfSets) {
      var _tmp = new Set();
      listOfSets.forEach( function(y) {
          for (var i of y) {
             _tmp.add(i);
          }
      });
      return _tmp;
    }

  /**
  *  Method to work out the intersection between two sets. 
  */
  function  calculateSetIntersect(setA, setB) {
      let _tmp = new Set();
      for (var i of setB) {
        if (setA.has(i)) {  
          _tmp.add(i); 
        }
      }
      return _tmp;
    }

    /**
    *  Method to get the set difference between set a and set b
    *  Return s a new set of the differences. 
    *  setA is the set returned from the intersection. 
    *
    */
    function calculateSetDifference(setA, setB) {
      let _t = new Set();
      for (var i of setB) {
        if (!setA.has(i)) {
           _t.add(i);
        }
      }
      return _t;
    }
  
   /**
   *  Method to calculate the Jaccard similarity
   */
   function jaccardSimilarity(setA, setB) {
     var intersect = this.calculateSetIntersect(setA, setB);
     var union = this.calculateSetUnion([setA, setB]);  
     return parseFloat(intersect.size / union.size);
   }

   /**
   * Method to show the similarities between two entities
   */
   function findSimilarity (entityA, entityB) {
      let set_A = _getData(entityA);
      let set_B = _getData(entityB);
      let t = this.calculateSetIntersect(set_A, set_B);
      clus.innerHTML = markUpEntityChanges(t,
             this.calculateSetDifference(t, set_B));
   }

   /**
   *  Method to extract the data object and ensure its a Set
   */
   function _getData(entity) {
      var _data;
      semdata.filter( function (y) {
       if (y.id == entity) {
           _data = new Set(y.data);
       }
    });
    return _data;
   }

   /**
   *  Method to create a mark up for the aggregations
   */
   function markUpAggregations(data) {
     html = '<ul id="aggregates">';
     data.forEach(
         function (d) { html += '<li>' + d.id + ' | ' + d.value + '</li>';  }
     );
     return html += '</ul></div>';
   }

   /**
   *  Called from the markup to show the similarities between an item 
   *  and other items in the result set. 
   */
   function markUpSimilarity(entityid) {
     html = '<ul id="similarities">';
     semdata.filter(
        function(d) {
            if (d.id == entityid) {
                d.similarity.forEach( function (y) { 
                  y.forEach(function(b) {  
                     html += "<li onclick='sims.findSimilarity(\""+ b[0] +"\", \""+ b[1]+"\")'>" 
                     + _findTitle(b[1]) + ':' + b[2] +  '</li>';
                  });  
              });
          }
     });
     html += '</ul></div>';
     clus.innerHTML = html; 
   }

   function markUpEntityChanges(set_union, set_difference) {
     _html = '<div id="similarities"><h3>Similarity</h3><ul>';
     set_union.forEach( function(d) {  _html += "<li>" + d.p + ' : ' + d.o + '</li>'; });
     _html += '</ul><h3>Difference</h3><ul>'
     set_difference.forEach( function(d) { _html += '<li>' + d.p + ' : ' + d.o + '</li>'; });
     return _html += '</ul></div>';
   }

   /**
   * Method to get the titles for the id.
   */
   function _findTitle (entity) {
      var _tmp = semdata.filter( function(d) { 
            if (d.id == entity) { return d.value; } 
      });
      return _tmp[0].value;
   }

   return {
     calculateSetUnion: calculateSetUnion,
     calculateSetIntersect: calculateSetIntersect,
     calculateSetDifference: calculateSetDifference,
     jaccardSimilarity: jaccardSimilarity, 
     findSimilarity: findSimilarity,
     markUpAggregations: markUpAggregations, 
     markUpSimilarity: markUpSimilarity
   }
}

