#!/usr/bin/env python


from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, DateTime

from datetime import datetime
from . import Base


class Gsheet(Base):
    __tablename__ = "gsheet"
    influence = Column(Integer)
    Naam = Column(String, primary_key=True)
    Bijgewerkt = Column(DateTime)
    CreditCap = Column(Integer)
    task = Column(String)
    WhitStar = Column(String)
    Transport = Column(String)
    TotalCargoSlots = Column(Integer)
    Miner = Column(String)
    HydrogenCapacity = Column(Integer)
    Battleship = Column(String)
    CargoBayExtension = Column(Integer)
    ShipmentComputer = Column(Integer)
    TradeBoost = Column(Integer)
    Rush = Column(Integer)
    TradeBurst = Column(Integer)
    ShipmentDrone = Column(Integer)
    Offload = Column(Integer)
    ShipmentBeam = Column(Integer)
    Entrust = Column(Integer)
    Dispatch = Column(Integer)
    Recall = Column(Integer)
    RelicDrone = Column(Integer)
    MiningBoost = Column(Integer)
    HydrogenBayExtension = Column(Integer)
    Enrich = Column(Integer)
    RemoteMining = Column(Integer)
    HydrogenUpload = Column(Integer)
    MiningUnity = Column(Integer)
    Crunch = Column(Integer)
    Genesis = Column(Integer)
    HydrogenRocket = Column(Integer)
    MiningDrone = Column(Integer)
    WeakBattery = Column(Integer)
    Battery = Column(Integer)
    Laser = Column(Integer)
    MassBattery = Column(Integer)
    DualLaser = Column(Integer)
    Barrage = Column(Integer)
    DartLauncher = Column(Integer)
    AlphaShield = Column(Integer)
    DeltaShield = Column(Integer)
    PassiveShield = Column(Integer)
    OmegaShield = Column(Integer)
    MirrorShield = Column(Integer)
    BlastShield = Column(Integer)
    AreaShield = Column(Integer)
    EMP = Column(Integer)
    Teleport = Column(Integer)
    RedStarLifeExtender = Column(Integer)
    RemoteRepair = Column(Integer)
    TimeWarp = Column(Integer)
    Unity = Column(Integer)
    Sanctuary = Column(Integer)
    Stealth = Column(Integer)
    Fortify = Column(Integer)
    Impulse = Column(Integer)
    AlphaRocket = Column(Integer)
    Salvage = Column(Integer)
    Suppress = Column(Integer)
    Destiny = Column(Integer)
    Barrier = Column(Integer)
    Vengeance = Column(Integer)
    DeltaRocket = Column(Integer)
    Leap = Column(Integer)
    Bond = Column(Integer)
    LaserTurret = Column(Integer)
    AlphaDrone = Column(Integer)
    Suspend = Column(Integer)
    OmegaRocket = Column(Integer)
    RemoteBomb = Column(Integer)

    def __repr__(self):
        return (
            f"<influence={self.influence},"
            f"Naam={self.Naam},"
            f"Bijgewerkt={self.Bijgewerkt},"
            f"CreditCap={self.CreditCap},"
            f"task={self.task},"
            f"WhitStar={self.WhitStar},"
            f"Transport={self.Transport},"
            f"TotalCargoSlots={self.TotalCargoSlots},"
            f"Miner={self.Miner},"
            f"HydrogenCapacity={self.HydrogenCapacity},"
            f"Battleship={self.Battleship},"
            f"CargoBayExtension={self.CargoBayExtension},"
            f"ShipmentComputer={self.ShipmentComputer},"
            f"TradeBoost={self.TradeBoost},"
            f"Rush={self.Rush},"
            f"TradeBurst={self.TradeBurst},"
            f"ShipmentDrone={self.ShipmentDrone},"
            f"Offload={self.Offload},"
            f"ShipmentBeam={self.ShipmentBeam},"
            f"Entrust={self.Entrust},"
            f"Dispatch={self.Dispatch},"
            f"Recall={self.Recall},"
            f"RelicDrone={self.RelicDrone},"
            f"MiningBoost={self.MiningBoost},"
            f"HydrogenBayExtension={self.HydrogenBayExtension},"
            f"Enrich={self.Enrich},"
            f"RemoteMining={self.RemoteMining},"
            f"HydrogenUpload={self.HydrogenUpload},"
            f"MiningUnity={self.MiningUnity},"
            f"Crunch={self.Crunch},"
            f"Genesis={self.Genesis},"
            f"HydrogenRocket={self.HydrogenRocket},"
            f"MiningDrone={self.MiningDrone},"
            f"WeakBattery={self.WeakBattery},"
            f"Battery={self.Battery},"
            f"Laser={self.Laser},"
            f"MassBattery={self.MassBattery},"
            f"DualLaser={self.DualLaser},"
            f"Barrage={self.Barrage},"
            f"DartLauncher={self.DartLauncher},"
            f"AlphaShield={self.AlphaShield},"
            f"DeltaShield={self.DeltaShield},"
            f"PassiveShield={self.PassiveShield},"
            f"OmegaShield={self.OmegaShield},"
            f"MirrorShield={self.MirrorShield},"
            f"BlastShield={self.BlastShield},"
            f"AreaShield={self.AreaShield},"
            f"EMP={self.EMP},"
            f"Teleport={self.Teleport},"
            f"RedStarLifeExtender={self.RedStarLifeExtender},"
            f"RemoteRepair={self.RemoteRepair},"
            f"TimeWarp={self.TimeWarp},"
            f"Unity={self.Unity},"
            f"Sanctuary={self.Sanctuary},"
            f"Stealth={self.Stealth},"
            f"Fortify={self.Fortify},"
            f"Impulse={self.Impulse},"
            f"AlphaRocket={self.AlphaRocket},"
            f"Salvage={self.Salvage},"
            f"Suppress={self.Suppress},"
            f"Destiny={self.Destiny},"
            f"Barrier={self.Barrier},"
            f"Vengeance={self.Vengeance},"
            f"DeltaRocket={self.DeltaRocket},"
            f"Leap={self.Leap},"
            f"Bond={self.Bond},"
            f"LaserTurret={self.LaserTurret},"
            f"AlphaDrone={self.AlphaDrone},"
            f"Suspend={self.Suspend},"
            f"OmegaRocket={self.OmegaRocket},"
            f"RemoteBomb={self.RemoteBomb}>"
        )
