(define (domain sokorobotto)
  (:requirements :typing)
  (:types pallette robot - phyobject
		  location - place
		  shipment order saleitem - object)
		  
  (:predicates (ships ?s - shipment ?o - order)
               (orders ?o - order ?si - saleitem)
               (packing-location ?l - place)
               (contains ?p - pallette ?si - saleitem)
               (at ?p - phyobject ?l - place)
               (includes ?sh - shipment ?si - saleitem)
               (unstarted ?sh - shipment)
               (available ?l - place)
               (free ?r - robot)
               (connected ?l ?l - place)
               (no-robot ?l - place)
               (no-pallette ?l - place)
  )
  
  (:action moveRobotWithPalletteToPackingLocation
      :parameters (?r - robot ?palletteLocation ?packingloc - location ?p - pallette)
      :precondition (and (at ?r ?palletteLocation) (at ?p ?palletteLocation) 
                         (no-robot ?packingloc) (no-pallette ?packingloc) (available ?packingloc) (packing-location ?packingloc)
                         (connected ?palletteLocation ?packingloc) (connected ?packingloc ?palletteLocation))
      :effect (and
          (at ?r ?packingloc) 
		  (at ?p ?packingloc)
		  (no-robot ?palletteLocation)
		  (no-pallette ?palletteLocation)
		  (not (no-robot ?packingloc))
		  (not (no-pallette ?packingloc))
		  (not (at ?r ?palletteLocation))
		  (not (at ?p ?palletteLocation))
		  (not (available ?packingloc))
      )
  )
  
  (:action load
      :parameters (?sh - shipment ?s - saleitem ?o - order ?r - robot ?p - pallette ?packingloc - location)
      :precondition (and (contains ?p ?s) (orders ?o ?s) (ships ?sh ?o) (at ?r ?packingloc) (at ?p ?packingloc) 
                         (packing-location ?packingloc))
      :effect (and
          (not (contains ?p ?s))
          (includes ?sh ?s)
          (at ?p ?packingloc)
      )
  )
  
  (:action moveRobotToOtherLocation
      :parameters (?r - robot ?from ?to - location)
      :precondition (and (at ?r ?from) (no-robot ?to) (connected ?from ?to))
      :effect (and
          (at ?r ?to) 
		  (no-robot ?from)
		  (not (no-robot ?to))
		  (not (at ?r ?from))
      )
  )
  
  (:action movePalletteToOtherLocation
      :parameters (?r - robot ?from ?to - location ?p - pallette)
      :precondition (and (at ?r ?from) (no-robot ?to) (no-pallette ?to) 
					(connected ?from ?to) (at ?p ?from) (not (packing-location ?from)) (not (packing-location ?to)))
      :effect (and
          (at ?r ?to) 
		  (at ?p ?to)
		  (no-robot ?from)
		  (no-pallette ?from)
		  (not (no-robot ?to))
		  (not (at ?r ?from))
		  (not (at ?p ?from))
		  (not (no-pallette ?to))
      )
  )
  
  (:action vacatePackingLocation
      :parameters (?r - robot ?packingLoc - location ?to - location ?p - pallette)
      :precondition (and (at ?r ?packingLoc) (no-robot ?to) (connected ?packingLoc ?to) (at ?p ?packingLoc)
                    (no-robot ?to) (no-pallette ?to) (packing-location ?packingLoc))
      :effect (and
          (at ?r ?to) 
		  (at ?p ?to)
		  (available ?packingLoc)
		  (no-robot ?packingLoc)
		  (no-pallette ?packingLoc)
		  (not (no-robot ?to))
		  (not (no-pallette ?to))
		  (not (at ?r ?packingLoc))
		  (not (at ?p ?packingLoc))
      )
  )
)