from diagram_lib import *

fig, ax = new_fig(1000, 760)

boundary(ax, 170, 70, 800, 640, "Justice Squad - Superhero Battle System")

# Actor
actor(ax, 70, 370, "Player")

# Use cases - left column
uc_recruit = usecase(ax, 330, 630, "Recruit Hero", w=160)
uc_gear = usecase(ax, 330, 540, "Equip Gear", w=160)
uc_alert = usecase(ax, 330, 450, "Respond to\nThreat Alert", w=170, h=54)
uc_retreat = usecase(ax, 330, 190, "Retreat from\nBattle", w=160, h=54)
uc_report = usecase(ax, 330, 110, "View HQ Report", w=170)

# Battle use case (parent) + children
uc_battle = usecase(ax, 620, 370, "Battle Villain\n(Take Turn)", w=190, h=70, fc="#fdf3e6", ec="#b9770e")
uc_attack = usecase(ax, 540, 230, "Attack", w=130)
uc_defend = usecase(ax, 690, 230, "Defend", w=130)
uc_ability = usecase(ax, 840, 270, "Use Ability", w=150)
uc_undo = usecase(ax, 840, 370, "Undo Action", w=150)

# secondary use case: villain counter-attack (system-side, included)
uc_counter = usecase(ax, 620, 510, "Villain\nCounter-Attack", w=170, h=58, fc="#fdecea", ec=RED)

# Associations from Player (one clean line to the border of each use case)
for uc in [uc_recruit, uc_gear, uc_alert, uc_retreat, uc_report]:
    association(ax, (95, 370), (uc.center[0] - uc.width / 2, uc.center[1]))
association(ax, (95, 370), (uc_battle.center[0] - uc_battle.width / 2, uc_battle.center[1]))
association(ax, (95, 370), (uc_undo.center[0] - uc_undo.width / 2, uc_undo.center[1] + 4))

# generalizations: Attack/Defend/UseAbility/Undo -> Battle Villain
generalization(ax, (uc_attack.center[0] + 10, uc_attack.center[1] + 23), (uc_battle.center[0] - 40, uc_battle.center[1] - 35))
generalization(ax, (uc_defend.center[0], uc_defend.center[1] + 23), (uc_battle.center[0] - 5, uc_battle.center[1] - 35))
generalization(ax, (uc_ability.center[0] - 10, uc_ability.center[1] + 29), (uc_battle.center[0] + 50, uc_battle.center[1] - 10))
generalization(ax, (uc_undo.center[0] - 30, uc_undo.center[1]), (uc_battle.center[0] + 95, uc_battle.center[1]))

# include: Respond to Threat Alert ..include.. Battle Villain
p1 = (uc_alert.center[0] + uc_alert.width / 2, uc_alert.center[1])
p2 = (uc_battle.center[0] - uc_battle.width / 2, uc_battle.center[1] + 10)
arrow(ax, p1, p2, style="-|>", dashed=True, color=NAVY)
label_mid(ax, p1, p2, "<<include>>", dy=10)

# include: Battle Villain ..include.. Villain Counter-Attack
p3 = (uc_battle.center[0] + 10, uc_battle.center[1] - uc_battle.height / 2)
p4 = (uc_counter.center[0] - 20, uc_counter.center[1] + uc_counter.height / 2)
arrow(ax, p3, p4, style="-|>", dashed=True, color=NAVY)
label_mid(ax, p3, p4, "<<include>>", dy=-22)

ax.text(170 + 800 / 2, 35, "Figure 2. Use Case Diagram - Justice Squad Superhero Battle",
        ha="center", va="bottom", fontsize=9, color="#555555")

save(fig, "usecase_diagram.png")
